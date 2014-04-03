from utils.args import subcommand_parser

if __name__ == "__main__":
    args = subcommand_parser.parse_args()
    args.func(args)