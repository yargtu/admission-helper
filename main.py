from calc import possible_specialties
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text
from config import TEST_TOKEN, DEMID_TOKEN
import uvloop

# bot = Bot(TEST_TOKEN)
bot = Bot(DEMID_TOKEN)




subject = ''
exams = []

# @bot.on.message(payload={"subject": "subject"})
# async def score_handler(message: Message) -> None:

#     global subject
#     subject = message.text

#     keyboard = Keyboard(one_time=True, inline=False).add(Text("Назад")).get_json()

#     await message.answer('Введите баллы', keyboard=keyboard)

@bot.on.message(payload={"subject": "subject"})
async def score_handler(message: Message) -> None:

    global subject
    exams.append(message.text)
    await subject_handler(message)

@bot.on.message(text=['О боте'])
async def score_handler(message: Message) -> None:

    ANSWER_TEXT = 'https://github.com/yargtu/admission-helper'

    KEYBOARD = (
            Keyboard(one_time=True)
            .add(Text("Назад", {"subject": "back"}))
            .get_json()
        )

    await message.answer(ANSWER_TEXT, keyboard=KEYBOARD)

@bot.on.message(payload={"subject": "subject"})
@bot.on.message(text=['Калькулятор ЕГЭ'])
async def subject_handler(message: Message) -> None:

    SUBJECTS = ("Математика", "Информатика", "История",
                "Обществознание", "Физика", "Химия",
                "Биология", "Литература")

    keyboard = Keyboard(one_time=True, inline=False)

    for i, subject in enumerate(SUBJECTS):
        keyboard.add(Text(subject, {"subject": "subject"}))
        if i % 2 != 0:
            keyboard.row()

    keyboard.add(Text("Назад", {"subject": "back"}))
    keyboard.add(Text("Далее", {"subject": "next"}))

    ANSWER_TEXT = 'Выберите экзамен, если все экзамены введены, нажмите "Далее"'

    await message.answer(ANSWER_TEXT, keyboard=keyboard.get_json())


@bot.on.message(payload={"subject": "back"})
async def back_subject_handler(message: Message) -> None:

    KEYBOARD = (
        Keyboard(one_time=True)
        .add(Text("Калькулятор ЕГЭ"))
        .add(Text("О боте"))
        .row()
        .add(Text("Задать вопрос"))
        .get_json()
    )

    await message.answer('Я вас категорически приветствую', keyboard=KEYBOARD)


@bot.on.message(payload={"subject": "next"})
async def calc_handler(message: Message) -> None:

    subject_specialties = possible_specialties(exams)
    ANSWER_TEXT = ''
    for faculty, specialties in subject_specialties.items():
        ANSWER_TEXT = '\n'.join((ANSWER_TEXT, f'{faculty}:\n'))
        for specialty in specialties:
            # ANSWER_TEXT = '\n'.join((specialty['Профиль'],))
            ANSWER_TEXT += specialty['Специальность'] + '\n'

    exams.clear()

    KEYBOARD = (
        Keyboard(one_time=True)
        .add(Text("Калькулятор ЕГЭ"))
        .add(Text("О боте"))
        .row()
        .add(Text("Задать вопрос"))
        .get_json()
    )
    await message.answer(ANSWER_TEXT, keyboard=KEYBOARD)


@bot.on.message()
async def main_handler(message: Message) -> None:
    global subject
    if subject and message.text != 'Назад':
        # print({"exam": subject, "score": message.text, "id": message.id})

        await subject_handler(message)
    else:
        ANSWER = 'Здесь вы можете задать свой вопрос'
        KEYBOARD = (
            Keyboard(one_time=True)
            .add(Text("Назад", {"subject": "back"}))
            .get_json()
        )
        await message.answer(ANSWER, keyboard=KEYBOARD)

if __name__ == '__main__':
    uvloop.install()
    bot.run_forever()
