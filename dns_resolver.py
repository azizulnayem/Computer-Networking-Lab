import dns.resolver
# DNS server address (e.g., Google's public DNS server)
DNS_SERVER = '8.8.8.8'

# Cache to store resolved domain names
cache = {}

def resolve_dns(domain):
    if domain in cache:
        return cache[domain]

    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [DNS_SERVER]

        answers = resolver.resolve(domain)
        ip_addresses = [str(rdata.address) for rdata in answers]

        cache[domain] = ip_addresses
        return ip_addresses
    except Exception as e:
        return f"Error: {str(e)}"

def create_dns_query(domain):
    query_id = 12345  # You can use a random number here
    flags = 0x0100   # Standard query, recursion desired
    qtype = 1        # A record type
    
    query = bytearray()
    query.extend((query_id >> 8, query_id & 0xFF))
    query.extend((flags >> 8, flags & 0xFF))
    query.extend((1, 0))  # Questions count
    query.extend((0, 0))  # Answer RRs
    query.extend((0, 0))  # Authority RRs
    query.extend((0, 0))  # Additional RRs
    for part in domain.split('.'):
        query.append(len(part))
        query.extend(part.encode())
    query.append(0)  # End of domain name
    
    query.extend((qtype >> 8, qtype & 0xFF))
    query.extend((0, 1))  # Class: IN
    
    return query

def send_dns_query(query):
    print("Sending DNS query:")
    print(query)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)
        client_socket.sendto(query, (DNS_SERVER, 53))
        response, _ = client_socket.recvfrom(1024)
        return response
    
def parse_dns_response(response):
    print("Parsing DNS response:")
    print(response)
    ip_addresses = []
    offset = 12  # Skip the DNS header
    qdcount = (response[4] << 8) + response[5]  # Question count
    
    for _ in range(qdcount):
        while response[offset] != 0:  # Skip domain name
            offset += 1
        offset += 5  # Skip QTYPE and QCLASS
    
    ancount = (response[6] << 8) + response[7]  # Answer count
    
    for _ in range(ancount):
        offset += 2  # Skip NAME
        rtype = (response[offset] << 8) + response[offset + 1]
        offset += 8  # Skip RDATA length and RDATA
        rdata_length = (response[offset] << 8) + response[offset + 1]
        offset += 2
        
        if rtype == 1:  # A record type
            ip = f"{response[offset]}.{response[offset + 1]}.{response[offset + 2]}.{response[offset + 3]}"
            ip_addresses.append(ip)
        
        offset += rdata_length
    
    return ip_addresses


def main():
    domain = input("Enter a domain name: ")
    ip_addresses = resolve_dns(domain)

    if isinstance(ip_addresses, list):
        print(f"IP addresses for '{domain}':")
        for ip in ip_addresses:
            print(ip)
    else:
        print(ip_addresses)

if __name__ == "__main__":
    main()
