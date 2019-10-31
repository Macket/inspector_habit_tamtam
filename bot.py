# -*- coding: UTF-8 -*-


from TamTamBot.TamTamBot import TamTamBot
from openapi_client import NewMessageBody, BotCommand, NewMessageLink, MessageLinkType
from openapi_client.models import StickerAttachment, StickerAttachmentPayload
from TamTamBot.utils.lng import set_use_django
from settings import TT_BOT_API_TOKEN
import users.intro as intro
import menu.handlers as menu
import plans.handlers as plans
from checks.handlers import handle_habit_report
from reminders.handlers import handle_audio
from users.data import preparing_habits, preparing_plans


class InspectorHabitBot(TamTamBot):
    @property
    def token(self):
        return TT_BOT_API_TOKEN

    @property
    def description(self):
        return '🇷🇺Инспектор Хэбит поможет вам приобрести полезные привычки и ' \
               'избавиться от вредных. А также этот бот будет полезен в планировании вашего дня.\n' \
               '🔥 Теперь можно создавать напоминания при помощи голосовых сообщений!\n\n' \
               '🇬🇧Inspector Habit will help you to develop good habits and break bad habits.' \
               'This bot will also be useful in planning your day.\n' \
               '🔥 Now you can create reminders via voice messages!'

    def get_commands(self):
        # type: () -> [BotCommand]
        commands = [BotCommand('menu', 'показать меню | display menu'),
                    BotCommand('today_plan', 'план на сегодня | plan for today')]
        return commands

    def send_message(self, user_id, message, keyboard=None, update=None):
        res = False
        if keyboard:
            try:
                res = self.view_buttons(message, keyboard, user_id=user_id, update=update)
            except:
                pass
        else:
            try:
                res = self.msg.send_message(NewMessageBody(message), user_id=user_id)
            except:
                pass
        return res

    def send_sticker(self, user_id, sticker_code):
        message_body = NewMessageBody()
        message_body.attachments = [StickerAttachment(
            payload=StickerAttachmentPayload(code=sticker_code),
            width=144,
            height=144,
        )]
        res = False
        try:
            res = self.msg.send_message(message_body, user_id=user_id)
        except:
            pass
        return res

    def forward_message(self, user_id, mid):
        link = NewMessageLink(MessageLinkType.FORWARD, mid)
        try:
            self.msg.send_message(NewMessageBody(link=link), user_id=user_id)
        except:
            pass

    def reply_message(self, user_id, mid, text, keyboard=None):
        link = NewMessageLink(MessageLinkType.REPLY, mid)
        mb = NewMessageBody(text, link=link)
        if keyboard:
            self.add_buttons_to_message_body(mb, keyboard)
        try:
            self.msg.send_message(mb, user_id=user_id)
        except:
            pass

    def edit_message(self, mid, text):
        res = False
        try:
            res = self.msg.edit_message(mid, NewMessageBody(text))
        except:
            pass
        return res

    def delete_message(self, mid):
        res = False
        try:
            res = self.msg.delete_message(mid)
        except:
            pass
        return res

    def receive_message(self, update):
        if update.user_id in preparing_plans:
            plans.handle_plan_append(bot, update)
            return True

        if update.message.body.attachments and update.message.body.attachments[0].type == 'location':
            if update.user_id in preparing_habits:  # Если пользователь отправил геопозицию при знакомстве с ботом
                intro.location_response(self, update)
                intro.habit_assign(self, update)
                return True
            else:  # Если пользователь отправил геопозицию в настройках
                menu.handle_location(self, update)
                menu.handle_main_menu(self, update)
                return False

        if update.message.body.attachments and update.message.body.attachments[0].type == 'sticker':
            print(update.message.body.attachments[0].payload.code)

        if update.message.body.attachments and update.message.body.attachments[0].type == 'audio':
            handle_audio(self, update)

    def cmd_handler_start(self, update):
        intro.register(self, update)
        return True

    def cmd_handler_set_lang(self, update):
        if not update.cmd_args:
            intro.language_request(self, update)
        else:
            intro.language_response(self, update)
        return False

    def cmd_handler_greeting(self, update):
        if not update.this_cmd_response:
            intro.greeting_and_habit_request(self, update)
            return True
        else:
            intro.habit_response(self, update)
            return False

    def cmd_handler_pick_days(self, update):
        intro.days_response(self, update)
        return False

    def cmd_handler_pick_time(self, update):
        if not update.this_cmd_response:
            intro.time_request(self, update)
        else:
            intro.time_response(self, update)
        return True

    def cmd_handler_pick_tz(self, update):
        if not update.cmd_args:
            intro.timezone_request(self, update)
            return False
        else:
            intro.timezone_response(self, update)
            intro.habit_assign(self, update)
            return True

    def cmd_handler_habit_report(self, update):
        handle_habit_report(self, update)
        return True

    def cmd_handler_menu(self, update):
        if update.this_cmd_response:
            if update.message.body.text.lower() in ['отмена', 'cancel']:
                menu.handle_main_menu(self, update)
            else:
                menu.handle_send_feedback(self, update)
                menu.handle_main_menu(self, update)
            return True
        elif not update.cmd_args:
            menu.handle_main_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'habits':
            menu.handle_habits_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'active_habits':
            menu.handle_active_habits(self, update)
            return False
        elif update.cmd_args['section'] == 'completed_habits':
            menu.handle_completed_habits(self, update)
            return False
        elif update.cmd_args['section'] == 'plans':
            menu.handle_plans_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'reminders':
            menu.handle_reminders_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'my_reminders':
            menu.handle_my_reminders(self, update)
            return False
        elif update.cmd_args['section'] == 'reminders_help':
            menu.handle_reminders_help(self, update)
            return False
        elif update.cmd_args['section'] == 'settings':
            menu.handle_settings_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'contact_developers':
            update.required_cmd_response = True
            menu.handle_contact_developers(self, update)
            return False
        elif update.cmd_args['section'] == 'language':
            menu.handle_language_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'language_change':
            menu.handle_language_change(self, update)
            menu.handle_main_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'timezone':
            menu.handle_timezone_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'pick_tz_menu':
            menu.handle_pick_tz_menu(self, update)
            return False
        elif update.cmd_args['section'] == 'pick_tz':
            menu.handle_pick_tz(self, update)
            menu.handle_main_menu(self, update)
            return False

    def cmd_handler_delete_habit(self, update):
        menu.handle_delete_habit(self, update)
        return True

    def cmd_handler_delete_reminder(self, update):
        menu.handle_delete_reminder(self, update)
        return True

    def cmd_handler_new_habit(self, update):
        if not update.this_cmd_response:
            menu.handle_new_habit(self, update)
            return True
        else:
            intro.habit_response(self, update)

    def cmd_handler_new_plan(self, update):
        plans.handle_new_plan(self, update)
        return False

    def cmd_handler_finish_plan(self, update):
        plans.handle_finish_plan(self, update)
        return False

    def cmd_handler_cancel_plan(self, update):
        plans.handle_cancel_plan(self, update)
        return False

    def cmd_handler_report_plan(self, update):
        plans.handle_report_plan(self, update)
        return False

    def cmd_handler_show_plan(self, update):
        plans.handle_show_plan(self, update)
        return False

    def cmd_handler_plan_item_change(self, update):
        plans.handle_plan_item_change(self, update)
        return False

    def cmd_handler_plan_item_report(self, update):
        res = plans.handle_plan_item_report(self, update)
        return res

    def cmd_handler_today_plan(self, update):
        plans.handle_today_plan(self, update)
        return True


set_use_django(False)
bot = InspectorHabitBot()
