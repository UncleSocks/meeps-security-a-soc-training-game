import pygame
import pygame_gui
import random
import sqlite3
import init
import sqlite
import elements.ticket_loop as ticket_loop


def ticket_creation(database):

    connect = sqlite3.connect(database, timeout=10)
    cursor = connect.cursor()

    window_surface, clock, background = init.pygame_init()
    manager = init.pygame_gui_init()

    threat_list = sqlite.threats(cursor)

    back_button = ticket_loop.back_button_func(manager)
    title_label, title_text_entry = ticket_loop.title_text_entry_func(manager)
    ticket_label, ticket_text_entry = ticket_loop.ticket_text_entry_func(manager)
    create_button, threat_entry_title_tbox, threat_entry_slist = ticket_loop.threat_entry_slist_func(manager, threat_list)
    threat_description_tbox = ticket_loop.threat_description_tbox_func(manager)


    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                   running = False

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == threat_entry_slist:
                    selected_threat = event.text
                    print(selected_threat)

                    cursor.execute('SELECT description, indicators, countermeasures FROM threats WHERE name=?', [selected_threat])
                    description, indicators, countermeasures = cursor.fetchone()
                    threat_description_tbox.set_text(f'<b>{selected_threat.upper()}</b>\n<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')

            ticket_title = title_text_entry.get_text()
            ticket_entry = ticket_text_entry.get_text()
            
            
        
            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()