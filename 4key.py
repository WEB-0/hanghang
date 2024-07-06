import streamlit as st
import openai

def request_chat_completion(
    prompt, 
    system_role="Your role is to be a competent teacher assistant.", 
    model="gpt-4o", 
    stream=False
):
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream
    )
    return response

def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "✒️")
        else:
            break
    placeholder.markdown(message)
    return message

st.set_page_config(
    page_title="과세특 도우미✍️",
    page_icon="✍️"
)

st.title("과세특 도우미🏫")
st.subheader("과세특 초안 작성기-제작 김가현👊")

# st.text_area('행발 키워드👇', "성격 및 태도 : 친절한/성실한/적극적인/밝은/신중한/침착한/책임감 있는/활기찬/창의적인/결단력 있는/유쾌한/온화한/관대한/호기심 많은/진취적인/열정적인/정직한/신뢰할 수 있는/외향적인/인내심 있는/협력적인/학구열이 높은/주도적인/규율을 잘 지키는/긍정적인/배려심 있는/끈기 있는/성취지향적인/열정적인                                                                                                                                                                                             학업 및 학습태도 : 우수한 성적을 유지함/꾸준히 발전함/학업에 열심히 노력함/목표를 향해 꾸준히 나아감/특정 과목에서 탁월한 성과를 보임/학습에 꾸준히 임함/성실하게 학습함/집중력이 뛰어남/명확한 목표를 가지고 학습함/학습 의지가 매우 높음/주제에 대해 깊이 있게 탐구함/창의적으로 문제를 해결함/협동심을 발휘하여 그룹 과제에 참여함/새로운 지식을 적극적으로 받아들임/스스로 학습 계획을 세우고 실천함/질문을 통해 이해를 높임/효과적인 시간 관리를 함/학습 자료를 철저히 준비함/피드백을 바탕으로 지속적으로 개선함                                                                                                                                                                                              학교 생활 및 생활습관 : 책임감 있게 역할을 수행함/친구들과 잘 어울림/리더십을 발휘함/학교 규칙을 잘 지킴동아리 활동에 적극적으로 참여함/예의를 갖추어 행동함/긍정적인 태도로 학교 생활을 즐김/규칙적인 생활 습관을 유지함/건강한 식습관을 실천함/정기적으로 운동을 함/효과적인 시간 관리를 함/개인 및 주변 환경의 청결을 유지함/정기적으로 독서를 함/스트레스를 효과적으로 관리함/긍정적인 사고 방식을 유지함/명확한 목표를 설정하고 실천함                                                                                                                                                                                              교우 관계 : 친구들과 잘 어울림/다양한 친구들과 원만한 관계를 유지함/협력적인 태도로 친구들을 도와줌/다른 학생들에게 존경심을 받음/새로운 친구를 사귀는 것을 즐김/팀 프로젝트에서 협동심을 발휘함/서로 배려하며 좋은 관계를 유지함/다른 사람의 의견을 존중함/친구들과의 갈등을 원만하게 해결함/즐겁고 활기찬 교우 관계를 유지함                                                                                                                                                                                              진로 및 진학 : 명확한 진로 목표를 설정함/진로 탐색 활동에 적극적으로 참여함/희망 대학 및 학과를 위해 철저히 준비함/체계적인 진로 계획을 수립하고 실천함/희망 진로와 관련된 활동에 참여함/진로에 필요한 역량을 개발함/진로 상담을 통해 방향을 설정함/목표 지향적으로 진학 준비를 함/자기 개발 활동을 꾸준히 실천함/희망 진로를 위해 학업에 열정을 쏟음")

auto_complete = st.toggle("👈누르면 예시가 나옵니다.")

example = {
    "subject": "국어",
    "study": "문학 작품 화자 바꾸기",
    "activity": "'엄마 걱정'작품을 읽고 화자를 바꿔서 시를 다시 씀.",
    "competency": "문화적 상상력이 돋보임."
}

prompt_template = """
학생의 교과 활동에 대해 종합의견을 작성해야합니다.
유저가 적은 내용을 바탕으로 종합의견을 언어 이음말 없이 자연스럽고 풍부하게 답변해주세요. 
반드시 모든 문장의 어미은 명사형으로 작성해야합니다.(~학생임, ~노력함)
예시1,2,3의 형식만을 참고해서 작성하고 문장은 간결하게 작성합니다.
[예시 1:국어 어휘의 다양한 체계와 양상을 정확히 이해하여 담화 상황에 적절하게 고유어, 한자어, 외래어의 선택을 달리하면서 어휘 체계의 특성 및 의미 관계와 변이에 따른 양상을 정확하게 활용함.
'진로 탐색을 위한 책 읽기' 활동에서는 진로 정보 탐색이라는 독서 목적에 따라 20명의 의사가 쓴 경험담을 읽고, 서로 다른 의학 전공의 세계에 흥미를 느낌. 지적 호기심이 풍부하여 언어 및
독서의 세계에서 새로운 사실을 발견하고 확인하는 것을 좋아함. 어휘의 체계와 양상에 대한 이해를 바탕으로 담화 상황에 적절한 어휘 사용하는 활동에서 지역 방언과 사회 방언을 담화 상황에
적절하게 활용하려고 노력함. '진로 탐색독서' 활동에서는 진로 정보 탐색이라는 독서 목적에 따라 본인이 관심 있는 직업인 정보보안전문가에 관한 책을 검색하여 신속하게 자료를 수집하는 능력을 보임. 자신의 정보 수집 능력을 활용하여 자료 수집에 어려움을 겪는 친구들을 도와주는 등 적극적인 모습을 보임.
예시 2:인수분해 공식에 대한 학습 과정 중 시행된 평가에서 필요한 원리를 정확히 이해하고 이를 활용하여 다양한 전략을 구사하는 등 유창성이 돋보임. 여러 가지 모형을 이용하여 인수분해 공식을 설명하는 활동
에서 삼차식의 인수분해를 입체도형과 연결하여 공감을 얻음. 평행이동, 대칭이동에 대한 개념을 정확히 이해하고 있으며 모둠활동에서 대칭성이 있는 그림그리기 과제를 조원들과 협력적인 상호작용을 통
해 모든 조원이 다양한 사례를 제시하는 분위기를 조성하고, 제시된 사례를 잘 정리하여 완성도있는 포스터 형태로 발표하는데 주도적인 역할을 함.
예시 3:영어성취도가 우수하며 지문독해 능력 및 발표에서 꾸준한 향상을 보임. 수업 후 예리한 질문을 하며 복습을 열심히 하는 모습이 인상적임. 인터넷 댓글 문화를 주제로 한토론활동에서 자신의 의견을 논리적
으로 구성해 제한된 시간 내에 자신감 있게 영어토론을 주도함. 영어 발표 시 내용의 흐름이 자연스럽고 어휘와 어법 사용에 오류가 거의 없이 완전한 문장을 사용하는 등 의사전달능력이 우수함. 영어로 자신의 의견을 표현할 때 청중이 알아듣기 쉽도록 제스처와 적절한 목소리톤을 사용해 효과적으로 발표함. '영어동화책 만들기'에서 익살스럽고 교훈이 담긴 'Angry Glue'라는 동화책을 만듦. 물감으로 직접 그림을 그리고 소품을 활용하여 완성도 높은 동화책을 완성했으며, 이야기를 파일에 녹음해 첨부하는 정성을 보임. 자신이 알고 있는 내용을 급우에게 쉽게 설명하려 노력하는 등 예비 초등 교사로서의 잠재력을 보여줌.
]


---
과목: {subject}
수업 주제: {study}
학생 활동: {activity}
성장모습: {competency}
---
""".strip()

with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input(
            "과목",
            value=example["subject"] if auto_complete else "",
            placeholder=example["subject"])
    with col2:
        study = st.text_input(
            "수업 주제",
            value=example["study"] if auto_complete else "",
            placeholder=example["study"])
    activity = st.text_area(
        "학생 활동",
        value=example["activity"] if auto_complete else "",
        placeholder=example["activity"])
    
    competency = st.text_area(
            "성장모습",
            value=example["competency"] if auto_complete else "",
            placeholder=example["competency"])

    
    submit = st.form_submit_button("작성하기")

if submit:
    if not subject:
        st.error("과목을 입력해주세요.")
    elif not study:
        st.error("수업 주제 또는 성취기준을 입력해주세요")
    elif not activity:
        st.error("학생의 활동 입력해주세요.")
    elif not competency:
        st.error("학생의 성장모습(역량)에 대해 입력해주세요.")
    else:
        prompt = prompt_template.format(
            subject=subject,
            study=study,
            activity=activity,
            competency=competency,
        )
        system_role = "Your role is to be a competent teacher assistant."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)
        st.markdown(f"**공백 포함 글자 수: {len(message)}**")
