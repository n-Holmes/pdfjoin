from src.joiner import concatenate


if __name__ == "__main__":
    paths = ["Chair Order.pdf", "Christmas Tickets.pdf", "Email Receipt.pdf"]
    details = {
        "Title": "Combined PDF Title",
        "Author": "someone",
        "Subject": "something",
        "Creator": "pdfjoin",
    }
    concatenate(paths, "concatenated.pdf", details)
