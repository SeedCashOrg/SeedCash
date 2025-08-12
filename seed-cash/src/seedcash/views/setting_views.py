from seedcash.gui.components import GUIConstants
from seedcash.views.view import (
    MainMenuView,
    View,
    Destination,
    BackStackView,
    RET_CODE__BACK_BUTTON,
)
from seedcash.gui.screens import setting_screens
from seedcash.gui.screens.screen import ButtonOption, WarningScreen
from seedcash.models.settings_definition import SettingsConstants

import logging

logger = logging.getLogger(__name__)


# Final Possible Load Seed View
class SettingOptionsView(View):
    LANGUAGE = ButtonOption("Language")
    SEED_PROTOCOL = ButtonOption("Seed Backup Protocol")
    TEST_BUTTONS = ButtonOption("Test Buttons")
    TEST_CAMERA = ButtonOption("Test Camera")
    CAMERA_ROTATION = ButtonOption("Camera Rotation")

    def __init__(self):
        super().__init__()

    def run(self):

        button_data = [
            self.LANGUAGE,
            self.SEED_PROTOCOL,
            self.TEST_BUTTONS,
            self.TEST_CAMERA,
            self.CAMERA_ROTATION,
        ]

        selected_menu_num = self.run_screen(
            setting_screens.SettingOptionsScreen,
            title="Settings",
            button_data=button_data,
        )
        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(MainMenuView)
        elif button_data[selected_menu_num] == self.LANGUAGE:
            return Destination(SettingLanguageView)
        elif button_data[selected_menu_num] == self.SEED_PROTOCOL:
            return Destination(SettingSeedProtocolView)
        elif button_data[selected_menu_num] == self.TEST_BUTTONS:
            return Destination(SettingTestButtons)
        elif button_data[selected_menu_num] == self.TEST_CAMERA:
            from seedcash.views.scan_view import ScanView

            return Destination(ScanView)
        elif button_data[selected_menu_num] == self.CAMERA_ROTATION:
            return Destination(CameraRotationOptionsView)


class SettingLanguageView(View):
    def __init__(self):
        super().__init__()

        # get all available languages
        self.available_languages = [
            lang[0] for lang in SettingsConstants.ALL_WORDLIST_LANGUAGES
        ]

        # Create button options for each available language
        self.language_buttons = [
            ButtonOption(lang[1]) for lang in SettingsConstants.ALL_WORDLIST_LANGUAGES
        ]

    def run(self):

        button_data = self.language_buttons

        selected_menu_num = self.run_screen(
            setting_screens.SettingOptionsScreen,
            title="Language",
            button_data=button_data,
        )
        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)
        elif button_data[selected_menu_num] in self.language_buttons:
            selected_language = self.available_languages[selected_menu_num]
            self.controller.settings.set_value(
                SettingsConstants.SETTING__WORDLIST_LANGUAGE, selected_language
            )
            logger.info(f"Language set to: {selected_language}")
            return Destination(BackStackView)


class SettingSeedProtocolView(View):
    def __init__(self):
        super().__init__()

        # Create button options for each seed protocol
        self.protocol_buttons = [
            ButtonOption(protocol[1])
            for protocol in SettingsConstants.ALL_SEED_PROTOCOLS
        ]

    def run(self):

        button_data = self.protocol_buttons
        selected_btn = ["BIP39", "SLIP39"].index(
            self.controller.settings.get_value(SettingsConstants.SETTING__SEED_PROTOCOL)
        )

        selected_menu_num = self.run_screen(
            setting_screens.SettingOptionsScreen,
            title="Seed Protocol",
            button_data=button_data,
            selected_button=selected_btn,
        )
        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)
        elif button_data[selected_menu_num] in self.protocol_buttons:
            selected_protocol = SettingsConstants.ALL_SEED_PROTOCOLS[selected_menu_num][
                0
            ]
            # if selected protocol is same as current, return to back stack
            if selected_protocol == self.controller.settings.get_value(
                SettingsConstants.SETTING__SEED_PROTOCOL
            ):
                return Destination(BackStackView)
            return Destination(
                ProtocolMigrationWarningView, view_args={"protocol": selected_protocol}
            )


class ProtocolMigrationWarningView(View):
    def __init__(self, protocol):
        self.protocol = protocol
        self.MIGRATE = ButtonOption("Migrate", button_label_color="red")
        self.buttons_data = [self.MIGRATE]
        super().__init__()

    def run(self):
        ret = self.run_screen(
            WarningScreen,
            title="Migrate Protocol?",
            status_headline="",
            text=(
                "BIP-39 and SLIP-39 are different and completely incompatible protocols."
            ),
            button_data=self.buttons_data,
            show_back_button=True,
        )

        if ret == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)
        elif self.buttons_data[ret] == self.MIGRATE:
            logger.info(f"User confirmed migration to protocol: {self.protocol}")
            self.controller.switch_seed_protocol(self.protocol)
            return Destination(BackStackView)


class SettingTestButtons(View):
    def run(self):
        self.run_screen(setting_screens.SettingTestButtonsScreen)

        return Destination(SettingOptionsView)


class CameraRotationOptionsView(View):
    def __init__(self):
        super().__init__()

        # Get Button Options for Camera Rotation
        self.camera_rotations = [
            ButtonOption(rotation[1])
            for rotation in SettingsConstants.ALL_CAMERA_ROTATIONS
        ]

    def run(self):

        button_data = self.camera_rotations
        selected_btn = [0, 90, 180, 270].index(
            self.controller.settings.get_value(
                SettingsConstants.SETTING__CAMERA_ROTATION
            )
        )

        selected_menu_num = self.run_screen(
            setting_screens.SettingOptionsScreen,
            title="Camera Rotation",
            button_data=button_data,
            selected_button=selected_btn,
        )
        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)
        elif button_data[selected_menu_num] in self.camera_rotations:
            selected_rotation = SettingsConstants.ALL_CAMERA_ROTATIONS[
                selected_menu_num
            ][0]
            self.controller.settings.set_value(
                SettingsConstants.SETTING__CAMERA_ROTATION, selected_rotation
            )
            return Destination(BackStackView)
