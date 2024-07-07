import paddle
from paddlespeech.cli.tts import TTSExecutor
tts_executor = TTSExecutor()
wav_file = tts_executor(
    text="""《西游记》全书共一百回，可分为四个长短不一的部分。开头诗为“混沌未分天地乱，茫茫渺渺无人见。自从盘古破鸿蒙，开辟从兹清浊辨。覆载群生仰至仁，发明万物皆成善。欲知造化会元功，须看《西游释厄传》。”第一部分是第一回至第七回，介绍故事主角孙悟空的诞生，孙悟空是吸收天地精华而生的石猴，因为向菩提祖师学法而得道，能通地煞七十二变、乘斤斗云、使如意金箍棒，他骄傲地自称为齐天大圣，桀骜不驯的行为让天庭十分头痛。在他大闹天宫之后，遭到如来佛祖降伏，如来佛祖将他压在五行山下长达五百年。""",
    output='output.wav',
    am='fastspeech2_male',
    am_config=None,
    am_ckpt=None,
    am_stat=None,
    spk_id=0,
    phones_dict=None,
    tones_dict=None,
    speaker_dict=None,
    voc='hifigan_male',
    voc_config=None,
    voc_ckpt=None,
    voc_stat=None,
    lang='zh',
    device=paddle.get_device())
print('Wave file has been generated: {}'.format(wav_file))