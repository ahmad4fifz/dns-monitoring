import argparse
import queue
import json
import dnstwist


#def csv(domains=[]):
#    csv = ["fuzzer,domain,dns_a,dns_aaaa,dns_mx,dns_ns,geoip"]
#    for domain in domains:
#        csv.append(
#            ",".join(
#                [
#                    domain.get("fuzzer"),
#                    domain.get("domain"),
#                    ";".join(domain.get("dns_a", [])),
#                    ";".join(domain.get("dns_aaaa", [])),
#                    ";".join(domain.get("dns_mx", [])),
#                    ";".join(domain.get("dns_ns", [])),
#                    domain.get("geoip", ""),
#                ]
#            )
#        )
#    return "\n".join(csv)

def out_json(domains=[]):
	return json.dumps(domains, indent=4, sort_keys=True)

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

    output = out_json(domains)

    return output


parser = argparse.ArgumentParser(description="Test for engine.py")
parser.add_argument("string", help="domain to query")
args = parser.parse_args()

print(dnx(args.string))
