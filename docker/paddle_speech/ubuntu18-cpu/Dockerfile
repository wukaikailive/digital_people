FROM python:3.9.19
LABEL maintainer="812166094@qq.com"

RUN pip3 install matplotlib==3.7.3
RUN pip3 install numpy==1.23.4
RUN pip3 install paddlepaddle==2.4.2
RUN pip3 install paddlespeech==1.4.1
RUN pip3 install protobuf==3.19.6
RUN pip3 install paddlenlp==2.5.2
RUN pip3 install scipy==1.11.4

WORKDIR /home/PaddleSpeech/
COPY application.yaml /home/PaddleSpeech/application.yaml
ADD nltk_data.tar /root

CMD ["paddlespeech_server","start","--config_file","/home/PaddleSpeech/application.yaml"]
