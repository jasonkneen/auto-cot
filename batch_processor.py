import argparse
from utils import *

def cot(method, question):
    args = parse_arguments()
    decoder = Decoder()

    args.method = method
    if args.method != "zero_shot_cot":
        if args.method == "auto_cot":
            args.demo_path = "demos/multiarith_auto"
        else:
            args.demo_path = "demos/multiarith_manual"
        demo = create_demo_text(args, cot_flag=True)
    else:
        demo = None

    x = "Q: " + question + "\n" + "A:"
    print('*****************************')
    print("Test Question:")
    print(question)
    print('*****************************')

    if args.method == "zero_shot":
        x = x + " " + args.direct_answer_trigger_for_zeroshot
    elif args.method == "zero_shot_cot":
        x = x + " " + args.cot_trigger
    elif args.method == "manual_cot":
        x = demo + x
    elif args.method == "auto_cot":
        x = demo + x + " " + args.cot_trigger
    else:
        raise ValueError("method is not properly defined ...")

    print("Prompted Input:")
    print(x.replace("\n\n", "\n").strip())
    print('*****************************')

    max_length = args.max_length_cot if "cot" in args.method else args.max_length_direct
    z = decoder.decode(args, x, max_length)
    z = z.replace("\n\n", "\n").replace("\n", "").strip()
    
    if args.method == "zero_shot_cot":
        z2 = x + z + " " + args.direct_answer_trigger_for_zeroshot_cot
        max_length = args.max_length_direct
        pred = decoder.decode(args, z2, max_length)
        output = z + " " + args.direct_answer_trigger_for_zeroshot_cot + " " + pred
        print("Output:")
        print(output)
        print('*****************************')
    else:
        pred = z
        output = pred
        print("Output:")
        print(output)
        print('*****************************')

    # Write to log file
    with open(f"{args.log_dir}/multiarith_zero_shot_cot.log", "a") as f:
        f.write(f"Q: {question}\n")
        f.write(f"A: {output}\n")
        f.write("\n")

    # Validate answer
    correct_answer = validate_answer(question, output)
    if correct_answer is not None:
        print(f"Answer Validation: {'Correct' if correct_answer else 'Incorrect'}")
        print('*****************************')

def validate_answer(question, output):
    # Extract numerical answer from output
    numbers = [int(s) for s in output.split() if s.isdigit()]
    if not numbers:
        return None
    
    # Calculate correct answer based on question
    if "10 friends" in question and "7 players quit" in question and "8 lives" in question:
        correct_answer = (10 - 7) * 8
        return numbers[-1] == correct_answer
    return None

def chat_interface():
    print("Welcome to the Zero-shot-CoT chat interface!")
    print("Type 'exit' to quit the chat.")
    while True:
        question = input("\nYou: ")
        if question.lower() == "exit":
            break
        print("\nModel:")
        cot("zero_shot_cot", question)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Zero-shot-CoT")

    parser.add_argument("--max_num_worker", type=int, default=0, help="maximum number of workers for dataloader")
    parser.add_argument(
        "--model", type=str, default="gpt-4o-mini", help="model used for decoding"
    )
    parser.add_argument(
        "--method", type=str, default="auto_cot", choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot", "auto_cot"], help="method"
    )
    parser.add_argument(
        "--cot_trigger_no", type=int, default=1, help="A trigger sentence that elicits a model to execute chain of thought"
    )
    parser.add_argument(
        "--max_length_cot", type=int, default=256, help="maximum length of output tokens by model for reasoning extraction"
    )
    parser.add_argument(
        "--max_length_direct", type=int, default=32, help="maximum length of output tokens by model for answer extraction"
    )
    parser.add_argument(
        "--limit_dataset_size", type=int, default=0, help="whether to limit test dataset size. if 0, the dataset size is unlimited and we use all the samples in the dataset for testing."
    )
    parser.add_argument(
        "--api_time_interval", type=float, default=1.0, help=""
    )
    parser.add_argument(
        "--temperature", type=float, default=0, help=""
    )
    parser.add_argument(
        "--log_dir", type=str, default="./log/", help="log directory"
    )
    args = parser.parse_args()

    args.direct_answer_trigger_for_fewshot = "The answer is"
    args.direct_answer_trigger_for_zeroshot = "The answer is"
    args.direct_answer_trigger_for_zeroshot_cot = "The answer is"
    args.cot_trigger = "Let's think step by step."

    return args

if __name__ == "__main__":
    chat_interface()