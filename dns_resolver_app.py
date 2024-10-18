import streamlit as st

import dns.resolver

# Function to resolve DNS queries
def dns_resolver(domain):
    result = {"IPv4": [], "IPv6": [], "Errors": ""}
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 4

        # Query for IPv4 (A) record
        result_A = resolver.resolve(domain, 'A')
        result["IPv4"] = [str(ip) for ip in result_A]

        # Query for IPv6 (AAAA) record
        result_AAAA = resolver.resolve(domain, 'AAAA')
        result["IPv6"] = [str(ip) for ip in result_AAAA]

    except dns.resolver.NoAnswer:
        result["Errors"] = f"No A or AAAA records found for {domain}"
    except dns.resolver.NXDOMAIN:
        result["Errors"] = f"Domain {domain} does not exist"
    except dns.resolver.Timeout:
        result["Errors"] = "Query timed out"
    except Exception as e:
        result["Errors"] = f"An error occurred: {e}"
    
    return result

# Streamlit app interface
st.title("Simple DNS Resolver")

# Input field for domain name
domain = st.text_input("Enter domain name:", "")

if st.button("Resolve"):
    if domain:
        st.write(f"Resolving DNS for: {domain}")
        result = dns_resolver(domain)

        # Display IPv4 and IPv6 results
        if result["IPv4"]:
            st.subheader("IPv4 Address(es):")
            for ip in result["IPv4"]:
                st.write(ip)

        if result["IPv6"]:
            st.subheader("IPv6 Address(es):")
            for ip in result["IPv6"]:
                st.write(ip)

        # Display Errors (if any)
        if result["Errors"]:
            st.error(result["Errors"])
    else:
        st.error("Please enter a domain name.")
