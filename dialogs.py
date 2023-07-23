import operator
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Next, Cancel, Button, Multiselect
from states import SettingState
from db.models import User, Settings
import constants


async def switch_to_next(m: Message,
                         text_widget: TextInput,
                         manager: DialogManager,
                         text: str):
    await manager.dialog().next()


async def switch_to_location(c: CallbackQuery,
                             b: Button,
                             manager: DialogManager):
    employment_types_widget: Multiselect = manager.dialog().\
        find('m_employment_type')
    checked_employment_types = employment_types_widget.\
        get_checked(manager=manager)
    LOCATION_REQUIRED_TYPES = (Settings.EMPLOYMENT_TYPE.HYBRID,
                               Settings.EMPLOYMENT_TYPE.OFFICE,
                               Settings.EMPLOYMENT_TYPE.RELOCATION)
    if any(typ in checked_employment_types for typ in LOCATION_REQUIRED_TYPES):
        await manager.switch_to(SettingState.locations)
    else:
        await manager.switch_to(SettingState.finish)


async def finish(c: CallbackQuery,
                 b: Button,
                 manager: DialogManager):
    skills: list[str] = [skill.strip() for skill in
                         manager.dialog().find('skills').
                         get_value().split(',')]
    locations: list[str] = [loc.strip() for loc in
                            manager.dialog().find('locations').
                            get_value().split(',')]
    levels: list[str] = manager.dialog().\
        find('m_levels').get_checked()
    emp_types: list[str] = manager.dialog().\
        find('m_employment_type').get_checked()
    user = User.objects.get(id=c.from_user)
    settings, created = Settings.objects.update_or_create(
        user=user,
        defaults=dict(
            level=levels,
            locations=locations,
            skills=skills,
            employment_type=emp_types)
        )
    await manager.mark_closed()


async def get_levels(**kwargs):
    return {"levels": Settings.LEVELS.choices}


async def get_employment_types(**kwargs):
    return {"employment_types": Settings.EMPLOYMENT_TYPE.choices}


async def get_choices(**kwargs):
    manager: DialogManager = kwargs['dialog_manager']
    skills: str = manager.dialog().find('skills').get_value()
    locations: str = manager.dialog().find('locations').get_value()
    levels: list[str] = manager.dialog().\
        find('m_levels').get_checked()
    emp_types: list[str] = manager.dialog().\
        find('m_employment_type').get_checked()
    return {"skills": skills,
            "locations": locations,
            "levels": ', '.join(levels),
            "emp_types": ', '.join(emp_types)}


start_window = Window(
    Const(constants.GREETING),
    Next(text=Const('Начать настройку')),
    Cancel(text=Const('❌Отменить')),
    state=SettingState.start)

skills_window = Window(
    Const(constants.SKILL),
    TextInput(id='skills', on_success=switch_to_next),
    state=SettingState.skills
    )

level_window = Window(
    Const(constants.LEVEL),
    Multiselect(id='m_levels',
                checked_text=Format("✅{item[0]}"),
                unchecked_text=Format("{item[0]}"),
                item_id_getter=operator.itemgetter(1),
                min_selected=1,
                items='levels'),
    Back(text=Const('Назад')),
    Next(text=Const('Продолжить')),
    Cancel(text=Const('❌Отменить')),
    state=SettingState.level,
    getter=get_levels
)

employment_type_window = Window(
    Const(constants.EMPLOYMENT),
    Multiselect(id='m_employment_type',
                checked_text=Format('✅{item[0]}'),
                unchecked_text=Format('{item[0]}'),
                item_id_getter=operator.itemgetter(1),
                min_selected=1,
                items='employment_types'),
    Back(text=Const('Назад')),
    Button(id='__next__',
           text=Const('Продолжить'),
           on_click=switch_to_location),
    Cancel(text=Const('❌Отменить')),
    state=SettingState.employment_type,
    getter=get_employment_types
)

locations_window = Window(
    Const(constants.LOCATION),
    Back(text=Const('Назад')),
    Cancel(text=Const('❌Отменить')),
    TextInput(id='locations', on_success=switch_to_next),
    state=SettingState.locations
)

finish_window = Window(
    Format("Навыки: {skills}\n"
           "Локации: {locations}\n"
           "Тип занятости: {emp_types}\n"
           "Уровень: {levels}"),
    Button(id='finish',
           text=Const('✅Всё верно'),
           on_click=finish),
    Back(text=Const('Назад')),
    Cancel(text=Const('❌Отменить')),
    state=SettingState.finish,
    getter=get_choices
)

settings_dialog = Dialog(start_window, skills_window,
                         level_window, employment_type_window,
                         finish_window, locations_window)
