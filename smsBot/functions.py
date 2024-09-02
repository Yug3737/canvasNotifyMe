carriers = {
    'att': 'txt.att.net', # AT&T
    'verizon': 'vtext.com', # Verizon
    'tmobile': 'tmomail.net', # T-Mobile
    'sprint': 'messaging.sprintpcs.com', # Sprint
    'spectrum': 'vtext.com', #Spectrum
    'uscellular': 'uscc.textmsg.com', #US Cellular
    'metropcs': 'metropcs.sms.us', # Metro PCS
    'mintmobile': 'tmomail.net',
}

def get_gateway_address(phone_number, carrier):
    return f"{phone_number}@{carriers[carrier]}"
