import queue

import dnstwist


def dnx(domain):
    url = dnstwist.UrlParser(domain)
    fuzz = dnstwist.Fuzzer(domain)
    fuzz.generate()

    jobs = queue.Queue()
    for j in fuzz.domains:
        jobs.put(j)

    global threads
    threads = []

    for i in range(dnstwist.THREAD_COUNT_DEFAULT * 30):
        worker = dnstwist.Scanner(jobs)
        worker.setDaemon(True)
        worker.uri_scheme = url.scheme
        worker.uri_path = url.path
        worker.uri_query = url.query
        worker.option_extdns = True
        worker.nameservers = ["1.1.1.1", "8.8.8.8"]
        worker.option_geoip = True

        worker.domain_orig = url.domain

        worker.start()
        threads.append(worker)

    worker = dnstwist.Scanner(jobs)
    worker.setDaemon(True)
    worker.start()
    worker.join()

    domains = fuzz.permutations(registered=True)

    return domains
