import pygame
import pygame_gui
import sqlite3
import init
import queries
import elements.threats_elements as threat_element


def threat_creation_init_values():

    threat_entry_name = None
    threat_entry_description = None
    threat_entry_indicators = None
    threat_entry_countermeasures = None
    threat_confirm_window = None

    return threat_entry_name, threat_entry_description, threat_entry_indicators, \
    threat_entry_countermeasures, threat_confirm_window


def threat_database_management(database):

    def threat_database_management_init(database):

        connect = sqlite3.connect(database, timeout=10)
        cursor = connect.cursor()

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        threat_list = queries.threats(cursor)
        threat_database_image_path = "Assets/threat_database.png"

        back_button = threat_element.back_button_func(manager)
        threat_database_image = threat_element.threat_database_image_func(manager, 
                                                                        threat_database_image_path)

        create_button, delete_button = threat_element.create_button_button_func(manager)
        threat_entry_title_tbox = threat_element.threat_entry_slist_misc_func(manager)
        threat_entry_slist = threat_element.threat_entry_slist_func(manager, threat_list)

        threat_details_label, selected_threat_title_tbox, selected_threat_description_tbox, \
            selected_threat_indicators_tbox, selected_threat_countermeasures_tbox, \
                selected_threat_image_path_tbox = threat_element.threat_details_func(manager)
        
        selected_threat = None

        return threat_database_management_loop(database, connect, cursor, 
                                            window_surface, clock, background, manager,
                                            threat_list, back_button, threat_database_image,
                                            create_button, delete_button,
                                            threat_entry_title_tbox, threat_entry_slist,
                                            threat_details_label, selected_threat_title_tbox, 
                                            selected_threat_description_tbox, selected_threat_indicators_tbox,
                                            selected_threat_countermeasures_tbox, selected_threat_image_path_tbox,
                                            selected_threat)

    def threat_database_management_loop(database, connect, cursor, 
                                        window_surface, clock, background, manager,
                                        threat_list, back_button, threat_database_image,
                                        create_button, delete_button,
                                        threat_entry_title_tbox, threat_entry_slist,
                                        threat_details_label, selected_threat_title_tbox, 
                                        selected_threat_description_tbox, selected_threat_indicators_tbox,
                                        selected_threat_countermeasures_tbox, selected_threat_image_path_tbox,
                                        selected_threat):

        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        running = False

                    if event.ui_element == create_button:
                        threat_list = threat_creation_init(database)
                        threat_entry_slist.kill()
                        threat_entry_slist = threat_element.threat_entry_slist_func(manager, threat_list)

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == threat_entry_slist:
                        selected_threat = event.text

                        cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
                        description, indicators, countermeasures, image_path = cursor.fetchone()

                        selected_threat_title_tbox.set_text(f"<b>{selected_threat}</b>")
                        selected_threat_description_tbox.set_text(f"DESCRIPTION:\n{description}")
                        selected_threat_indicators_tbox.set_text(f"INDICATORS:\n{indicators}")
                        selected_threat_countermeasures_tbox.set_text(f"COUNTERMEASURES:\n{countermeasures}")
                        selected_threat_image_path_tbox.set_text(f"{image_path}")

                if selected_threat is not None:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == delete_button:
                            
                            cursor.execute('DELETE FROM tickets WHERE answer=?', [selected_threat])
                            connect.commit()
                            cursor.execute('DELETE FROM threats WHERE name=?', [selected_threat])
                            connect.commit()

                            threat_list = queries.threats(cursor)
                            threat_entry_slist.kill()
                            threat_entry_slist = threat_element.threat_entry_slist_func(manager, threat_list)

                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    def threat_creation_init(database):

        connect = sqlite3.connect(database, timeout=10)
        cursor = connect.cursor()

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        add_threat_image_path = "Assets/add_threat.png"
        add_threat_image = threat_element.add_threat_image_func(manager, add_threat_image_path)

        back_button = threat_element.back_button_func(manager)
        add_button = threat_element.threat_entry_add_button_func(manager)

        threat_entry_name_tentry, threat_entry_description_tentry, threat_entry_indicators_tentry, \
            threat_entry_countermeasures_tentry, threat_entry_image_path_tentry = threat_element.threat_entry_func(manager)
        
        threat_entry_name, threat_entry_description, threat_entry_indicators, \
            threat_entry_countermeasures, threat_confirm_window = threat_creation_init_values()
        
        return threat_creation_loop(connect, cursor, window_surface, clock, background, manager,
                                    add_threat_image, back_button, add_button, threat_entry_name_tentry, 
                                    threat_entry_description_tentry, threat_entry_indicators_tentry,
                                    threat_entry_countermeasures_tentry, threat_entry_image_path_tentry,
                                    threat_entry_name, threat_entry_description, threat_entry_indicators,
                                    threat_entry_countermeasures, threat_confirm_window)
        

    def threat_creation_loop(connect, cursor, window_surface, clock, background, manager, 
                             add_threat_image, back_button, add_button, threat_entry_name_tentry, 
                             threat_entry_description_tentry, threat_entry_indicators_tentry, 
                             threat_entry_countermeasures_tentry, threat_entry_image_path_tentry, 
                             threat_entry_name, threat_entry_description, threat_entry_indicators, 
                             threat_entry_countermeasures, threat_confirm_window):
        
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        updated_threat_list = queries.threats(cursor)
                        return updated_threat_list

                threat_entry_name = threat_entry_name_tentry.get_text()
                threat_entry_description = threat_entry_description_tentry.get_text()
                threat_entry_indicators = threat_entry_indicators_tentry.get_text()
                threat_entry_countermeasures = threat_entry_countermeasures_tentry.get_text()
                threat_entry_image_path = threat_entry_image_path_tentry.get_text()

                if threat_entry_name is not None and threat_entry_description is not None and threat_entry_indicators is not None and threat_entry_countermeasures is not None:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == add_button:

                            cursor.execute('SELECT MAX(id) FROM threats')
                            last_id = cursor.fetchone()[0]
                            new_id = last_id + 1

                            new_threat = (new_id, threat_entry_name, threat_entry_description, threat_entry_indicators, threat_entry_countermeasures, threat_entry_image_path)
                            cursor.execute('INSERT INTO threats VALUES (?, ?, ?, ?, ?, ?)', new_threat)
                            connect.commit()

                            threat_confirm_window, threat_confirm_close_button = threat_element.threat_confirm_window_func(manager)

                manager.process_events(event)

            manager.update(time_delta)
            window_surface.blit(background, (0, 0))

            if threat_confirm_window:
                threat_confirm_window.show()
                manager.draw_ui(window_surface)

                for event in pygame.event.get():
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == threat_confirm_close_button:

                            threat_entry_name_tentry.set_text("")
                            threat_entry_description_tentry.set_text("")
                            threat_entry_indicators_tentry.set_text("")
                            threat_entry_countermeasures_tentry.set_text("")

                            threat_confirm_window.hide()

                            threat_entry_name, threat_entry_description, threat_entry_indicators, \
                                threat_entry_countermeasures, threat_confirm_window = threat_creation_init_values()
                        
                    manager.process_events(event)

            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    threat_database_management_init(database)   