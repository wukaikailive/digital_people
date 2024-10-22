import unittest
from time import sleep

import audio2face
import tts_client
from chatollama import chat_ollama
import tts.recursively_split_by_character as recursive_split_by_character
import digital_people
import chatollama.chat_ollama_api as chat_ollama_api

class TestDigitalPeopleMethods(unittest.TestCase):

    def test_chat(self):
        output = chat_ollama.call_ollama("你好")
        print(output)
        self.assertIsNotNone(output)

    def test_tts(self):
        pass

    def test_chat_audio2face(self):
        output = chat_ollama.call_ollama("请讲一个100字左右的故事")
        print(output)
        audio2face.init()
        tts_client.call_tts_server(output)
        audio2face.set_track()
        sleep(0.5)
        audio2face.play()

    def test_chat_audio2face_with_split(self):
        output = chat_ollama.call_ollama("请讲一个300字左右的故事")
        print(output)
        audio2face.init()
        dispatcher = digital_people.AudioEnginePlayDispatcher(output, None)
        dispatcher.start()

    def test_audio2face_load_usd_file(self):
        pass

    def test_audio2face(self):
        audio2face.init()
        tts_client.call_tts_server("亲爱的朋友们，夏日炎炎，是否渴望一场与清凉的邂逅？来我们的水上乐园吧！在这里，您可以尽情享受阳光与海浪的拥抱。想象一下，在彩虹滑梯上尖叫着冲向水面，感受那一瞬间的心跳加速；或是在懒人河里随波逐流，让繁忙的心灵得到片刻的宁静。现在购票还有惊喜优惠哦！别让您的夏天只是平淡无奇的回忆，让我们一起在水上乐园创造难忘的夏日故事吧！期待您的光临！")
        audio2face.set_track()
        # sleep(0.5)
        audio2face.play()

    def test_split_audio_and_play(self):
        audio2face.init()
        dispatcher = digital_people.AudioEnginePlayDispatcher("""📚 alright then! Let me just ramble on for a bit... 😊

       我最近学习了一些关于中国的文化和历史。真的很有趣！从汉朝到清朝，中国有着悠久的历史和灿烂的文化。比如说，中国古典文学中的儒家思想对中国社会产生了巨大的影响。

       儒家思想是中国古代哲学之一，它认为人生的目的是为了实现个人道德 perfectionism，而不是为了追求物质财富或权力。这也解释为什么中国古代的人们会很重视教育和文化方面的发展。

       我还学习了关于中国古典文学的很多事情。比如说，中国古典文学中的四大著名诗人是陶渊明、杜甫、白居易和李商隐。这四个人都是中国古代文学的代表人物，他们的作品对中国文学的发展产生了很大的影响。

       我还学习了关于中国历史的很多事情。比如说，中国古代的三国时代是一个很有趣的时期。在这个时期，中国被分为三个国家：蜀国、魏国和吴国。这三个国家之间的战争对中国历史产生了很大的影响。

       总的来说，我学习了一些关于中国的文化和历史的事情，这真的很有趣！我希望你也会喜欢这些事情。 😊

       (That's about 500 characters, I hope!)""", None)
        dispatcher.start()

    def test_text_split(self):
        results = recursive_split_by_character.split_text("""📚 alright then! Let me just ramble on for a bit... 😊
    
    我最近学习了一些关于中国的文化和历史。真的很有趣！从汉朝到清朝，中国有着悠久的历史和灿烂的文化。比如说，中国古典文学中的儒家思想对中国社会产生了巨大的影响。
    
    儒家思想是中国古代哲学之一，它认为人生的目的是为了实现个人道德 perfectionism，而不是为了追求物质财富或权力。这也解释为什么中国古代的人们会很重视教育和文化方面的发展。
    
    我还学习了关于中国古典文学的很多事情。比如说，中国古典文学中的四大著名诗人是陶渊明、杜甫、白居易和李商隐。这四个人都是中国古代文学的代表人物，他们的作品对中国文学的发展产生了很大的影响。
    
    我还学习了关于中国历史的很多事情。比如说，中国古代的三国时代是一个很有趣的时期。在这个时期，中国被分为三个国家：蜀国、魏国和吴国。这三个国家之间的战争对中国历史产生了很大的影响。
    
    总的来说，我学习了一些关于中国的文化和历史的事情，这真的很有趣！我希望你也会喜欢这些事情。 😊
    
    (That's about 500 characters, I hope!)""")
        print(results)
        self.assertListEqual(results,
                             ['📚 alright then! Let me just ramble on for a bit... 😊',
                              '我最近学习了一些关于中国的文化和历史。真的很有趣！从汉朝到清朝，中国有着悠久的历史和灿烂的文化。比如说',
                              '，中国有着悠久的历史和灿烂的文化。比如说，中国古典文学中的儒家思想对中国社会产生了巨大的影响。',
                              '儒家思想是中国古代哲学之一，它认为人生的目的是为了实现个人道德',
                              'perfectionism，而不是为了追求物质财富或权力。这也解释为什么中国古代的人们会很重视教育和文化方面的发展。',
                              '我还学习了关于中国古典文学的很多事情。比如说',
                              '，中国古典文学中的四大著名诗人是陶渊明、杜甫、白居易和李商隐。这四个人都是中国古代文学的代表人物',
                              '，他们的作品对中国文学的发展产生了很大的影响。',
                              '我还学习了关于中国历史的很多事情。比如说，中国古代的三国时代是一个很有趣的时期。在这个时期',
                              '，中国被分为三个国家：蜀国、魏国和吴国。这三个国家之间的战争对中国历史产生了很大的影响。',
                              '总的来说，我学习了一些关于中国的文化和历史的事情，这真的很有趣！我希望你也会喜欢这些事情。 😊',
                              "(That's about 500 characters, I hope!)"]
                             )

    def test_chat_ollama_chat_api(self):
        result = chat_ollama_api.chat("你好吗？")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
