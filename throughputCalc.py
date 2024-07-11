from math import ceil

STANDARDS = {1: "g", 2: "ac_w2", 3: "ax"}
RATES = {1: "maximum", 2: "minimum"}
PROTOCOLS = {1: "UDP", 2: "TCP"}

PARAMS = {
    "g": {"minimum": 24, "maximum": 216, "symbolTransmitTime": 4, "frameSizeBits": 12342, "SIFS": 10, "preamble": 20, "signalExtension": 6, "TCPAck": 662},
    "ac_w2": {"minimum": [26, 1872], "maximum": [346, 24960], "symbolTransmitTime": 3.6, "frameSizeBits": 12390, "SIFS": 16, "preamble": 92.8, "signalExtension": 0, "TCPAck": 710},
    "ax": {"minimum": [117, 7840], "maximum": [1950, 130666], "symbolTransmitTime": 13.6, "frameSizeBits": 12390, "SIFS": 16, "preamble": 92.8, "signalExtension": 0, "TCPAck": 710}
}

def calculate_throughput(protocol, standard, rate, case):
    slot_time = 9
    standard_params = PARAMS[standard]
    
    sifs = standard_params["SIFS"]
    bits_per_symbol = standard_params[rate]
    preamble = standard_params["preamble"]
    transmit_time = standard_params["symbolTransmitTime"]
    signal_extend = standard_params["signalExtension"]
    frame_size = standard_params["frameSizeBits"]
    tcp_ack_size = standard_params["TCPAck"]
  
    difs = (2 * slot_time) + sifs
    
    if standard == "g":
        bits_per_symbol = standard_params[rate]
    else:
        bits_per_symbol = standard_params[rate][0 if case == "normal" else 1]
    
    payload_symbols = ceil(frame_size / bits_per_symbol)
    tcp_ack_symbols = ceil(tcp_ack_size / bits_per_symbol)
    payload_frame_time = payload_symbols * transmit_time
    tcp_ack_frame_time = tcp_ack_symbols * transmit_time
    
    if protocol == "UDP":
        time_total = difs + preamble + transmit_time + signal_extend + sifs + preamble + transmit_time + signal_extend + sifs \
            + preamble + payload_frame_time + signal_extend + sifs + preamble + transmit_time + signal_extend   
    else:
        time_total = difs + preamble + transmit_time + signal_extend + sifs + preamble + transmit_time + signal_extend + sifs \
            + preamble + payload_frame_time + signal_extend + sifs + preamble + transmit_time + signal_extend \
            + difs + preamble + transmit_time + signal_extend + sifs + preamble + transmit_time + signal_extend + sifs \
            + preamble + tcp_ack_frame_time + signal_extend + sifs + preamble + transmit_time + signal_extend   

    return 12000 / time_total

def calculate_transfer_time(throughput):
    bytes_to_transfer = 15_000_000_000
    bits_to_transfer = bytes_to_transfer * 8
    throughput_bps = throughput * 1_000_000
    return bits_to_transfer / throughput_bps

def get_user_choice(prompt, options):
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and int(choice) in options:
            return int(choice)
        print("Invalid choice. Please try again.")

def main():
    standard = STANDARDS[get_user_choice("\nSelect a standard:", STANDARDS)]
    rate = RATES[get_user_choice("\nSelect a data rate:", RATES)]
    protocol = PROTOCOLS[get_user_choice("\nSelect a protocol:", PROTOCOLS)]

    if standard == "g":
        throughput = calculate_throughput(protocol, standard, rate, "none")
        print(f"\nThroughput: {throughput:.2f} Mbps")
        transfer_time = calculate_transfer_time(throughput)
        print(f"Time to transfer 15 x 10^9 bytes: {transfer_time:.0f} seconds")
    else:
        for case in ["normal", "best"]:
            throughput = calculate_throughput(protocol, standard, rate, case)
            print(f"\n{case.capitalize()} Case Throughput: {throughput:.2f} Mbps")
            transfer_time = calculate_transfer_time(throughput)
            print(f"Time to transfer 15 x 10^9 bytes in {case} case: {transfer_time:.0f} seconds")

if __name__ == "__main__":
    while True:
        main()
        if get_user_choice("\nDo you want to do another calculation?", {1: "Yes", 2: "No"}) != 1:
            break