# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
import configparser
import struct
import os
import re
import codecs
import logging
import fnmatch
import shutil
# -------------------------------------------------------------------

class collectfiles(object):

        self.dir_filters = {
                            'dat': re.compile('.*(\.dat|\.txt)$'),
                            'csv': re.compile('.*(\.csv)$'),
                            'sta': re.compile('.*(\.sta|\.ste|\.ini|\.ecs)$'),
                            'cfg': re.compile('.*(ych|yce|ini|cfg)$'),
                            'knop': re.compile('.*(\.tuf|\.dfm|\.cpp|\.h|\.ddp)$'),
                            'tuf': re.compile('.*(\.tuf|\.dfm)$'),
                            'ett': re.compile('.*(\.csv|\.ettlist)$'),
                            'other': re.compile('.*(windnc\.ini|tulist.bin)$')
                            }
        self.select_dnc_ = re.compile('.*(dnc_)')
        self.list_all_file_db_sta = {
                                    'cfg': set(),
                                    'csv': set(),
                                    'sta': set(),
                                    'dat': set(),
                                    'ett': set()
                                    }
        file_list = ('dac',)
        for add_file in file_list:
            self.list_all_file_db_sta['cfg'].add(add_file)
        self.ste_parser = configparser.ConfigParser()
        self.struct_ych = '>i13s13s10b'
        self.list_DuplicateError = []

    def split_dir(self, dir_dnc_, file_in_dnc_):
        try:
            before_dir, after_dir = re.split('db_sta|.db_sta', dir_dnc_)
            create_dir = 'db_sta{0}'.format(after_dir)
            if not os.path.exists(create_dir):
                os.makedirs(create_dir.lower())

            copy_file_in = os.path.join(dir_dnc_, file_in_dnc_)
            shutil.copyfile(
                copy_file_in,
                os.path.join(
                    create_dir,
                    file_in_dnc_.lower()))
            print('!!!Copy file  {0}'.format(copy_file_in.lower()))
        except Exception as e:
            logging.error(e)
        return

    def walk_dbsta(self, scan_dir):
        for root, dirs_walk, files in os.walk(scan_dir):
            if not self.select_dnc_.match(root.lower()):
                for d in dirs_walk:
                    if d.lower() in self.dir_filters:
                        key = d.lower()
                        dir_walk = os.path.join(root, d)
                        for f in os.listdir(dir_walk):
                            if os.path.isfile(
                                    os.path.join(
                                        dir_walk,
                                        f)) and self.dir_filters[key].match(
                                    f.lower()):
                                yield (key, dir_walk, f)
        return

    def copy_dnc(self, root_open_dir):
        for root, dirs_walk, files in os.walk(root_open_dir):
            for d in dirs_walk:
                dir_walk = os.path.join(root, d)
                if d.lower() in self.dir_filters:
                    key = d.lower()
                else:
                    key = 'other'
                if self.select_dnc_.match(dir_walk.lower()):
                    for f in os.listdir(dir_walk):
                        if os.path.isfile(
                                os.path.join(
                                    dir_walk,
                                    f)) and self.dir_filters[key].match(
                                f.lower()):
                            yield (dir_walk, f)

    # -------------------------------------------------------------------

    def add_list_file(self, key, ini_file):
        self.list_all_file_db_sta[key].add(ini_file)

    def get_list_file(self, key):
        return self.list_all_file_db_sta.get(key)

    # -------------------------------------------------------------------


    # -------------------------------------------------------------------

    def pars_file_ych(self, root_open_dir):
        for root_dir, search_ych_file, file in os.walk(root_open_dir):
            for search_ych_file in search_ych_file:
                d = os.path.join(root_dir, search_ych_file)
                if not self.select_dnc_.match(d.lower()):
                    if search_ych_file.lower() in 'cfg':
                        set_file = set()
                        for fy in os.listdir(d):
                            exp = os.path.splitext(fy)[1].lower()
                            if exp.endswith('.ych') or exp.endswith('.yce'):
                                set_file.add(fy.lower())

                        for file_ych_open in set_file & self.get_list_file('cfg'):
                            self.open_sta(root_dir, file_ych_open)
            self.list_all_file_db_sta['ett'] = self.list_all_file_db_sta['sta']
            list_tmp = set()
            for r in self.get_list_file('cfg'):
                list_tmp.add(os.path.splitext(r)[0])
            self.list_all_file_db_sta['cfg'] = list_tmp

            try:
                for root_dir, dir_copy, file in self.walk_dbsta(root_open_dir):
                    name_file, expt = os.path.splitext(file)
                    if name_file.lower() in self.list_all_file_db_sta.get(
                            root_dir):
                        self.split_dir(dir_copy, file)
            except Exception as e:
                logging.error(e)
            return

    def pars_dnc_(self, root_open_dir):
        for dir_dnc_, file_in_dnc_ in self.copy_dnc(root_open_dir):
            if file_in_dnc_.lower() in 'windnc.ini':
                self.pars_WinDnc_ini(os.path.join(dir_dnc_, file_in_dnc_))
            self.split_dir(dir_dnc_, file_in_dnc_)
        self.pars_file_ych(root_open_dir)
        for error_windnc_ini in self.list_DuplicateError:
            print('------------------------------')
            print(error_windnc_ini)

    def pars_WinDnc_ini(self, path_windnc_ini):
        try:

            self.ini_parser.read(path_windnc_ini)

            for section in self.ini_parser.sections():
                if not section.find('Настройки Полигона'):
                    self.add_list_file('cfg',os.path.basename(self.ini_parser.get(section,'file')).lower())
            for option_ini_file in self.ini_parser.options('Виды')[1:-1]:
                paremetr_windnc_ini = re.split(
                    ';|->|Участок:',
                    self.ini_parser.get(
                        'Виды',
                        option_ini_file))
                file_csv = paremetr_windnc_ini[3]
                if file_csv:
                    self.list_all_file_db_sta['csv'].add(file_csv.lower())

        except configparser.DuplicateSectionError as error:

            self.list_DuplicateError.append(
                'NameFile:{0}\nERROR: DuplicateSectionError\nsection: {1}'
                .format(path_windnc_ini, error.section))
        except configparser.DuplicateOptionError as error:
            # self.ini_parser.remove_option("TN", "TNSlotToAS")
            self.list_DuplicateError.append(
                'NameFile:{0}\nERROR: DuplicateOptionError\nsection: {1}\noption: {2}' .format(
                    path_windnc_ini,
                    error.section,
                    error.option))
        except configparser.NoOptionError as error:
            self.list_DuplicateError.append(
                'NameFile:{0}\nERROR: NoOptionError\nsection: {1}\noption: {2}'.format(
                    path_windnc_ini,
                    error.section,
                    error.option))
        except configparser.NoSectionError as error:
            self.list_DuplicateError.append(
                'NameFile:{0}\nERROR: NoSectionError\nsection: {1}'.format(
                    path_windnc_ini,
                    error.section))
        self.ini_parser.clear()
        # -------------------------------------------------------------------

    def open_sta(self, key, file_ych_open):
        path_ych = os.path.join(key, 'cfg', file_ych_open)
        try:
            if fnmatch.fnmatch(file_ych_open, '*.ych'):

                size_file = os.path.getsize(path_ych) - 2
                with open(path_ych, 'rb') as ych_file:
                    while size_file > ych_file.tell():
                        size_struct_ych = ych_file.read(
                            struct.calcsize(
                                self.struct_ych))
                        text_ych = struct.unpack_from(
                            self.struct_ych,
                            size_struct_ych)
                        ini_file = text_ych[1].decode('cp866')
                        ini_file = ini_file[:ini_file.find('\x00')]
                        self.add_list_file('sta', ini_file.lower())
                        self.ini_parser.read(os.path.join(key,'sta','%s.ini' %(ini_file)))
                        for option_ini_file in self.ini_parser.options('Chanels'):
                            ini_file = self.ini_parser.get('Chanels',option_ini_file)
                            self.add_list_file('dat', ini_file.lower())
                print('!!!Open file_ych %s' % (path_ych))

            elif fnmatch.fnmatch(file_ych_open, '*.yce'):
                ste_parser = configparser.ConfigParser()
                self.ini_parser.clear()
                if os.path.exists(path_ych):
                    with codecs.open(path_ych, encoding='cp866', mode='r') as yce_file:
                        self.ini_parser.read_file(yce_file)
                        for section in self.ini_parser.sections():
                            if not section.find('STATION_'):
                                file_ste = self.ini_parser.get(section,bytes('смfilename',
                                        encoding='cp1251').decode('cp866')).lower()
                                ste_parser.clear()
                                with codecs.open(os.path.join(key, 'sta', file_ste), encoding='cp866',
                                                 mode='r') as ste_file:
                                    ste_parser.read_file(ste_file)
                                    for option_ste_file in ste_parser.options('STATION'):
                                        if not option_ste_file.find('chanel_'):
                                            name_chanel = ste_parser.get('STATION',option_ste_file)
                                            self.add_list_file('dat',name_chanel.lower())
                                self.add_list_file('sta',os.path.splitext(file_ste)[0])
                ste_parser.clear()
        except Exception as e:
            logging.error(e)
            print('!!!Can not open file  %s' % (file_ych_open))

        return
