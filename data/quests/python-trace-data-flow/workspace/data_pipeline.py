def transform_v1(s):
    return s.upper()

def transform_v2(s):
    return f"IDENT:{s}-PROCESSED"

def transform_v3(s):
    return f"{s}-V2"

def process_pipeline(input_val):
    step1 = transform_v1(input_val)
    step2 = transform_v2(step1)
    step3 = transform_v3(step2)
    return step3

if __name__ == "__main__":
    # What is the result for 'foundry-v1'?
    pass
