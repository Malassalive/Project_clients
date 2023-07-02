import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

st.title('Добро пожаловать на борт "Будущего"!')

st.divider()

st.image('https://sun9-80.userapi.com/impg/gF4mV0V0bhpxbNFbR2O7SY79mKuNbH9vag5CxA/wV1DaZTOysQ.jpg?size=1280x606&quality=96&sign=a1103ad30bc40b00841a98417b085079&type=album')
st.header('"Будущее уже здесь!" -')
st.caption('так гласит слоган нашей компании. У Вас есть уникальная возможность оценить удовлетворенность перелетом, который Вам только предстоит преодолеть, заполнив совсем немного информации о себе и о своих ожиданиях')
st.divider()

eda = st.checkbox('Разведочный анализ данных')
if (eda ==True):
    st.caption('Для обучения модели был предложен датасет на 128 тысяч строк. Однако в данных были явные выбросы и аномалии, которые могли исказить качество модели')
    st.caption('Например, посмотрим на распределение возраста пассажиров до и после работы над датасетом')
    DATASET_PATH = "https://raw.githubusercontent.com/evgpat/edu_stepik_from_idea_to_mvp/main/datasets/clients.csv"
    df0 = pd.read_csv(DATASET_PATH)
    df00 = df0[['id','Age']]
    fut = st.radio('Перемещение во времени',['Было','Стало'],horizontal = True)
    if (fut =='Было'):
        st.vega_lite_chart(df00, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'id', 'type': 'quantitative'},
            'y': {'field': 'Age', 'type': 'quantitative'},
            }})
    else: 
        z = abs(stats.zscore(df00[['Age']], nan_policy='omit'))
        df_after = df00[(z<3).all(axis=1)]
        df_after = df_after[df_after['Age'] != 0]
        st.vega_lite_chart(df_after, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'id', 'type': 'quantitative'},
            'y': {'field': 'Age', 'type': 'quantitative'},
            }})
    st.caption('Данные были отфильтрованы с помощью Z-оценки, все значения, выходящие за трехсигмовые границы, были удалены, как и нулевые значения')
    st.caption('И так нужно было сделать со всеми числовыми данными о деталях перелета. Так, были данные о перелете, длина которого составляла 7,5 полных оборотов вокруг Земли, а время задержки рейса - 15 дней. Может быть эти кейсы были реальны, мы не знаем. Однако определенно уверены в том, что это вряд ли похоже на что-то обыденное')
st.divider()

st.sidebar.header('Ваши данные')
gender = st.sidebar.radio('Пол',['Male','Female'])
age = st.sidebar.number_input('Возраст',0,100)
loyalty = st.sidebar.radio('Вы лояльный клиент?',['Loyal Customer','disloyal Customer'])
typefl = st.sidebar.selectbox('Тип перелета',['Business travel','Personal Travel'])
classfl = st.sidebar.selectbox('Класс перелета',['Eco','Eco Plus','Business'])
distance = st.sidebar.slider('Длина перелета',0, 5000)
delayarr = st.sidebar.slider('Задержка рейса в минутах',0, 500)
delaydep = st.sidebar.slider('Задержка прибытия в минутах',0, 500)

st.header('Персональные данные')
st.text('Вы можете заполнить Ваши данные и информацию о деталях перелета на боковой панели')
st.caption('Не забудьте проверить достоверность введенных данных!')
df = pd.DataFrame({'Gender': [gender],'Age':[age],'Customer Type':[loyalty],'Type of Travel':[typefl],'Flight Distance':[distance],"Departure Delay in Minutes":[delayarr],"Arrival Delay in Minutes":[delaydep],})
edited = st.data_editor(df,num_rows = 1)
if (typefl == 'Business travel'):
    st.text('Желаем успехов в грядущем бизнес-трипе!')
else:
    st.text('Приятного путешествия!')

st.divider()

st.header('Параметры перелета')
choice = st.radio('Выберите способ оценки',['Вручную','Я не хочу оценивать самостоятельно'])
if (choice == 'Вручную'):
    st.caption('Перед Вами открылся лист оценки по шкале от 0 до 5 баллов. Проиграйте сценарий полета в голове: как вы приходите на посадку, как стюард или стюардесса приносит аппетитный ланч, как вы смотрите любимый фильм на спинке кресла перед вами. Представили? А теперь оцените Ваш опыт!')
    st.text('Лист оценивания:')
    col1,col2 = st.columns(2)
    df1 = pd.DataFrame({'Inflight wifi service': [col1.radio('Важность Wi-Fi',[0,1,2,3,4,5], horizontal=True)],
                       'Departure/Arrival time convenient':[col1.radio('Удобство время вылета и прибытия',[0,1,2,3,4,5], horizontal=True)],
                       'Ease of Online booking':[col1.radio('Оцените Wi-Fi',[0,1,2,3,4,5], horizontal=True)],
                       'Gate location':[col1.radio('Расположение гейта',[0,1,2,3,4,5], horizontal=True)],
                       "Food and drink":[col1.radio('Еда и напитки на борту',[0,1,2,3,4,5], horizontal=True)],
                       "Online boarding":[col1.radio('Онлайн регистрация',[0,1,2,3,4,5], horizontal=True)],
                       'Seat comfort':[col1.radio('Удобство кресла',[0,1,2,3,4,5], horizontal=True)],
                       'Inflight entertainment':[col2.radio('Развлечения на борту',[0,1,2,3,4,5], horizontal=True)],
                        'On-board service':[col2.radio('Бортовое обслуживание',[0,1,2,3,4,5], horizontal=True)],
                        'Leg room service':[col2.radio('Место для ног',[0,1,2,3,4,5], horizontal=True)],
                        'Baggage handling':[col2.radio('Место для ручной клади',[0,1,2,3,4,5], horizontal=True)],
                        'Checkin service':[col2.radio('Регистрация на рейс',[0,1,2,3,4,5], horizontal=True)],
                        'Inflight service':[col2.radio('Обслуживание в полете',[0,1,2,3,4,5], horizontal=True)],
                        'Cleanliness':[col2.radio('Чистота салона',[0,1,2,3,4,5], horizontal=True)],}).T
    edited = st.data_editor(df1, width=500)
    st.caption('Проверьте Ваши оценки!')
    st.line_chart(df1)




if (choice == 'Я не хочу оценивать самостоятельно'):
    st.text('Будущее уже здесь, Вы же ещё не успели это забыть? ')
    st.caption('Наш умнейший искусственный интеллект проставил оценки за вас! :sunglasses:')
    st.caption('_Всегда с заботой о Вас и о Вашем времени,_')
    st.caption('_"Будущее"_')
    df1 = pd.DataFrame({'Inflight wifi service': [np.random.randint(0,6)],
                       'Departure/Arrival time convenient':[np.random.randint(0,6)],
                       'Ease of Online booking':[np.random.randint(0,6)],
                       'Gate location':[np.random.randint(0,6)],
                       "Food and drink":[np.random.randint(0,6)],
                       "Online boarding":[np.random.randint(0,6)],
                       'Seat comfort':[np.random.randint(0,6)],
                       'Inflight entertainment':[np.random.randint(0,6)],
                        'On-board service':[np.random.randint(0,6)],
                        'Leg room service':[np.random.randint(0,6)],
                        'Baggage handling':[np.random.randint(0,6)],
                        'Checkin service':[np.random.randint(0,6)],
                        'Inflight service':[np.random.randint(0,6)],
                        'Cleanliness':[np.random.randint(0,6)],
                       
                       }).T
    edited = st.data_editor(df1,num_rows = 1, width = 500)
    st.caption('Посмотрите на получившиеся оценки!')
    st.line_chart(df1)

model = pd.read_pickle('https://github.com/Malassalive/Project_clients/raw/main/model_no_norm.pickle')

df_test = pd.concat([df,df1.T], sort=False, axis =1)

df_test['Gender'] = df_test['Gender'].map({'Male' : 1, 'Female' : 0})
df_test['Customer Type'] = df_test['Customer Type'].map({'Loyal Customer' : 1, 'disloyal Customer' : 0})
df_test['Type of Travel'] = df_test['Type of Travel'].map({'Business travel' : 1, 'Personal Travel' : 0})

st.divider()

st.header('Теперь нажимай на кнопку ниже!')
st.text('Загляни в свое будущее')
if (st.button('Узнать ответ')):
    st.text('Полученные нами данные')
    st.dataframe(df_test)
    answer = model.predict(df_test)
    proba = model.predict_proba(df_test)
    
    if (answer == 1):
        prob1 = proba[0,1].round(2)
        st.write('Вам понравится Ваш полет с вероятностью', prob1*100,'%!')
        st.image('https://sun9-15.userapi.com/impg/8VPTmI9JJ2nQZZU9f_P00oxVh33zdEmHI6Ufug/azzIiU94SVg.jpg?size=1280x572&quality=96&sign=7598dd763590810f85e5fc70c527d4dc&type=album')
    else: 
        prob0 = proba[0,0].round(2)
        st.image('https://sun9-50.userapi.com/impg/0ZYozZI5Ge9upp_DzJSltxJAx0zKfTFgdDGeDg/GXnJhCnQuxs.jpg?size=1280x607&quality=96&sign=48c8205529ccd527dd87f4f936fe54cd&type=album')
        st.write('Полет оставит вас равнодушным с вероятностью', prob0*100,'% :(')

        