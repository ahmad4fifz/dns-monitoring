from queue import Queue
from time import time
from uuid import uuid4

from dnstwist import Fuzzer, Scanner, UrlParser

try:
    import idna.codec
except ImportError:
    pass

THREADS = 10
SESSION_TTL = 300
SESSION_MAX = 20

DICTIONARY = (
    "auth",
    "account",
    "confirm",
    "connect",
    "enroll",
    "http",
    "https",
    "info",
    "login",
    "mail",
    "my",
    "online",
    "payment",
    "portal",
    "recovery",
    "register",
    "ssl",
    "safe",
    "secure",
    "signin",
    "signup",
    "support",
    "update",
    "user",
    "verify",
    "verification",
    "web",
    "www",
)
TLD_DICTIONARY = (
    "com",
    "net",
    "org",
    "info",
    "cn",
    "co",
    "eu",
    "de",
    "uk",
    "pw",
    "ga",
    "gq",
    "tk",
    "ml",
    "cf",
    "app",
    "biz",
    "top",
    "xyz",
    "online",
    "site",
    "live",
)


class Session:
    def __init__(self, url, nameserver=None, thread_count=THREADS):
        self.id = str(uuid4())
        self.timestamp = int(time())
        self.url = UrlParser(url)
        self.nameserver = nameserver
        self.thread_count = thread_count
        self.jobs = Queue()
        self.threads = []
        fuzz = Fuzzer(
            self.url.domain, dictionary=DICTIONARY, tld_dictionary=TLD_DICTIONARY
        )
        fuzz.generate()
        self.permutations = fuzz.permutations()

    def scan(self):
        for domain in self.permutations:
            self.jobs.put(domain)
        for _ in range(self.thread_count):
            worker = Scanner(self.jobs)
            worker.setDaemon(True)
            worker.option_extdns = True
            worker.option_geoip = True
            if self.nameserver:
                worker.nameservers = [self.nameserver]
            worker.start()
            self.threads.append(worker)

    def stop(self):
        self.jobs.queue.clear()
        for worker in self.threads:
            worker.stop()
            worker.join()
        self.threads.clear()

    def domains(self):
        domains = [x for x in self.permutations.copy() if x.is_registered()]

        def _idna(item):
            try:
                item["domain"] = item["domain"].encode().decode("idna")
            except Exception:
                pass
            return item

        return list(map(_idna, domains))

    def status(self):
        if self.jobs.empty():
            self.stop()
        total = len(self.permutations)
        remaining = max(self.jobs.qsize(), len(self.threads))
        complete = total - remaining
        registered = sum([1 for x in self.permutations if x.is_registered()])
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "url": self.url.full_uri(),
            "total": total,
            "complete": complete,
            "remaining": remaining,
            "registered": registered,
        }

    def csv(self):
        csv = ["fuzzer,domain,dns_a,dns_aaaa,dns_ns,dns_mx,geoip"]
        for domain in list([x for x in self.permutations if x.is_registered()]):
            csv.append(
                ",".join(
                    [
                        domain.get("fuzzer"),
                        domain.get("domain"),
                        domain.get("dns_a", [""])[0],
                        domain.get("dns_aaaa", [""])[0],
                        domain.get("dns_ns", [""])[0],
                        domain.get("dns_mx", [""])[0],
                        domain.get("geoip", ""),
                    ]
                )
            )
        return "\n".join(csv)

    def json(self):
        return [x for x in self.permutations if x.is_registered()]

    def list(self):
        return "\n".join([x.get("domain") for x in self.permutations])
