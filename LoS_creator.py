# -*- coding:utf-8 -*-

import sys
# from PyQt4.QtGui import *
from PyQt4.Qt import *

__author__ = 'Gree-gorey'


class SetDiffer(QWidget):
    def __init__(self):
        super(SetDiffer, self).__init__()
        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')

        # создаем главный грид
        main_layout = QGridLayout()

        def start():
            TwoListsWindow()
            # print arguments_list1.currentIndex()
            # print cb.checkState(), button_group.checkedId()

        def exit_f():
            self.close()

        def about():
            w = QWidget()
            QMessageBox.about(w, u'About', u'LoS creator version 0.1\n'
                                           u'author: gree-gorey\n'
                                           u'repository: https://github.com/gree-gorey/listOfStimuli_creator')
            self.show()

        # создаем поле кнопок
        groupBox = QGroupBox()
        hbox = QHBoxLayout()

        # Add a button
        start_btn = QPushButton(u'Создать ...')
        start_btn.setToolTip(u'Нажмите, чтобы начать создавать листы')
        start_btn.clicked.connect(start)
        # btn.resize(btn.sizeHint())

        # Add a button
        exit_btn = QPushButton(u'Выход')
        exit_btn.setToolTip(u'Нажмите, чтобы завершить работу')
        exit_btn.clicked.connect(exit_f)
        # btn.resize(btn.sizeHint())

        # Add a button
        about_btn = QPushButton(u'О программе ...')
        # about_btn.setToolTip(u'Нажмите, чтобы составить листы')
        about_btn.clicked.connect(about)
        # btn.resize(btn.sizeHint())

        # Приветствие
        gr = QLabel(u'Это альфа-версия программы LoS creator\n'
                    u'Возможны баги')

        hbox.addWidget(start_btn)
        hbox.addWidget(exit_btn)
        hbox.addWidget(about_btn)
        groupBox.setLayout(hbox)

        # добавляем виджеты в грид
        main_layout.addWidget(gr, 1, 1)
        main_layout.addWidget(groupBox, 2, 1)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class TwoListsWindow(QWidget):
    def __init__(self):
        super(TwoListsWindow, self).__init__()
        self.initUI()

    def initUI(self):
        # self.resize(500, 500)
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')

        # задаем шрифты
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        pos_font = QFont()
        pos_font.setBold(True)
        pos_font.setPointSize(18)

        # создаем главный грид
        main_layout = QGridLayout()

        ############
        # ЛИСТ 1
        ############

        groupBox = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        verbs = QRadioButton(u'Глаголы')
        verbs.setFont(pos_font)
        nouns = QRadioButton(u'Существительные')
        nouns.setFont(pos_font)
        list_1_pos = QButtonGroup()
        list_1_pos.addButton(verbs, 1)
        list_1_pos.addButton(nouns, 2)
        label_list1 = QLabel(u'Лист 1\n')
        label_list1.setAlignment(Qt.AlignHCenter)
        label_list1.setFont(title_font)
        vbox.addWidget(label_list1)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        arguments_list1 = QComboBox()
        arguments_list1.addItem(u'любые')
        arguments_list1.addItem(u'только один аргумент')
        arguments_list1.addItem(u'только два аргумента')
        vbox.addWidget(arguments_list1)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        reflexivity_list1 = QComboBox()
        reflexivity_list1.addItem(u'любые')
        reflexivity_list1.addItem(u'только возвратные')
        reflexivity_list1.addItem(u'только невозвратные')
        vbox.addWidget(reflexivity_list1)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        instrumentality_list1 = QComboBox()
        instrumentality_list1.addItem(u'любые')
        instrumentality_list1.addItem(u'только инструментальные')
        instrumentality_list1.addItem(u'только неинструментальные')
        vbox.addWidget(instrumentality_list1)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        relation_list1 = QComboBox()
        relation_list1.addItem(u'любые')
        relation_list1.addItem(u'только соотнесенные')
        relation_list1.addItem(u'только несоотнесенные')
        vbox.addWidget(relation_list1)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        part_list1 = QComboBox()
        part_list1.addItem(u'любые')
        part_list1.addItem(u'только из первой части')
        part_list1.addItem(u'только из второй части')
        vbox.addWidget(part_list1)

        # завершаем ЛИСТ 1
        groupBox.setLayout(vbox)

        ############
        # ЛИСТ 2
        ############

        groupBox2 = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        verbs = QRadioButton(u'Глаголы')
        verbs.setFont(pos_font)
        nouns = QRadioButton(u'Существительные')
        nouns.setFont(pos_font)
        list_2_pos = QButtonGroup()
        list_2_pos.addButton(verbs, 1)
        list_2_pos.addButton(nouns, 2)
        label_list2 = QLabel(u'Лист 2\n')
        label_list2.setAlignment(Qt.AlignHCenter)
        label_list2.setFont(title_font)
        vbox.addWidget(label_list2)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        arguments_list1 = QComboBox()
        arguments_list1.addItem(u'любые')
        arguments_list1.addItem(u'только один аргумент')
        arguments_list1.addItem(u'только два аргумента')
        vbox.addWidget(arguments_list1)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        reflexivity_list1 = QComboBox()
        reflexivity_list1.addItem(u'любые')
        reflexivity_list1.addItem(u'только возвратные')
        reflexivity_list1.addItem(u'только невозвратные')
        vbox.addWidget(reflexivity_list1)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        instrumentality_list1 = QComboBox()
        instrumentality_list1.addItem(u'любые')
        instrumentality_list1.addItem(u'только инструментальные')
        instrumentality_list1.addItem(u'только неинструментальные')
        vbox.addWidget(instrumentality_list1)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        relation_list1 = QComboBox()
        relation_list1.addItem(u'любые')
        relation_list1.addItem(u'только соотнесенные')
        relation_list1.addItem(u'только несоотнесенные')
        vbox.addWidget(relation_list1)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        part_list1 = QComboBox()
        part_list1.addItem(u'любые')
        part_list1.addItem(u'только из первой части')
        part_list1.addItem(u'только из второй части')
        vbox.addWidget(part_list1)

        # завершаем ЛИСТ 2
        groupBox2.setLayout(vbox)

        def go():
            # if cb_differ.checkState():
                # self.close()
            SetDiffer()
                # , button_group.checkedId()

        # def differ():
        #     pass

        # добавляем чек для разных листов
        cb_differ = QCheckBox(u'Листы должны отличаться на один параметр')
        # cb_differ.toggled.connect(differ)

        # Add a button
        btn = QPushButton(u'Далее >')
        btn.setToolTip(u'Нажмите, чтобы составить листы')
        btn.clicked.connect(go)
        # btn.resize(btn.sizeHint())

        # добавляем виджеты в грид
        main_layout.addWidget(groupBox, 1, 1, 1, 2)
        main_layout.addWidget(groupBox2, 1, 3, 1, 2)
        main_layout.addWidget(cb_differ, 2, 2, 1, 2)
        # main_layout.setColumnStretch(0, 2)
        main_layout.addWidget(btn, 3, 2, 1, 2)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartWindow(QWidget):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')

        # создаем главный грид
        main_layout = QGridLayout()

        def start():
            TwoListsWindow()
            # print arguments_list1.currentIndex()
            # print cb.checkState(), button_group.checkedId()

        def exit_f():
            self.close()

        def about():
            w = QWidget()
            QMessageBox.about(w, u'About', u'LoS creator version 0.1\n'
                                           u'author: gree-gorey\n'
                                           u'repository: https://github.com/gree-gorey/listOfStimuli_creator')
            self.show()

        # создаем поле кнопок
        groupBox = QGroupBox()
        hbox = QHBoxLayout()

        # Add a button
        start_btn = QPushButton(u'Создать ...')
        start_btn.setToolTip(u'Нажмите, чтобы начать создавать листы')
        start_btn.clicked.connect(start)
        # btn.resize(btn.sizeHint())

        # Add a button
        exit_btn = QPushButton(u'Выход')
        exit_btn.setToolTip(u'Нажмите, чтобы завершить работу')
        exit_btn.clicked.connect(exit_f)
        # btn.resize(btn.sizeHint())

        # Add a button
        about_btn = QPushButton(u'О программе ...')
        # about_btn.setToolTip(u'Нажмите, чтобы составить листы')
        about_btn.clicked.connect(about)
        # btn.resize(btn.sizeHint())

        # Приветствие
        gr = QLabel(u'Это альфа-версия программы LoS creator\n'
                    u'Возможны баги')

        hbox.addWidget(start_btn)
        hbox.addWidget(exit_btn)
        hbox.addWidget(about_btn)
        groupBox.setLayout(hbox)

        # добавляем виджеты в грид
        main_layout.addWidget(gr, 1, 1)
        main_layout.addWidget(groupBox, 2, 1)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    # StartWindow()
    # TwoListsWindow()
    SetDiffer()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
