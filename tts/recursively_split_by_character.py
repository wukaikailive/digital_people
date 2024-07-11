from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    chunk_size=60,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    # Existing args
)


def split_text(text):
    """
    对文本进行拆分断句
    :param text:
    :return:
    """
    return text_splitter.split_text(text)


if __name__ == '__main__':
    texts = split_text("""📚 alright then! Let me just ramble on for a bit... 😊
    
    我最近学习了一些关于中国的文化和历史。真的很有趣！从汉朝到清朝，中国有着悠久的历史和灿烂的文化。比如说，中国古典文学中的儒家思想对中国社会产生了巨大的影响。
    
    儒家思想是中国古代哲学之一，它认为人生的目的是为了实现个人道德 perfectionism，而不是为了追求物质财富或权力。这也解释为什么中国古代的人们会很重视教育和文化方面的发展。
    
    我还学习了关于中国古典文学的很多事情。比如说，中国古典文学中的四大著名诗人是陶渊明、杜甫、白居易和李商隐。这四个人都是中国古代文学的代表人物，他们的作品对中国文学的发展产生了很大的影响。
    
    我还学习了关于中国历史的很多事情。比如说，中国古代的三国时代是一个很有趣的时期。在这个时期，中国被分为三个国家：蜀国、魏国和吴国。这三个国家之间的战争对中国历史产生了很大的影响。
    
    总的来说，我学习了一些关于中国的文化和历史的事情，这真的很有趣！我希望你也会喜欢这些事情。 😊
    
    (That's about 500 characters, I hope!)""")
    print(texts)
