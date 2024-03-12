import pygame
import pygame_gui
import random
import init
import elements.main_loop_elements as main_loop_elements
from queries import ticket_ids, threats


def start_shift(connect, cursor):

    def start_shift_init(connect, cursor):

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        ticket_ids_list = ticket_ids(cursor)
        total_tickets = len(ticket_ids_list)
        threat_list = threats(cursor)

        ticket_timer = 0
        randomized_ticket_entry = random.uniform(2, 3)
        popup_window_close_timer = 0
        popup_window_sla_countdown = 15
        
        main_sla_timer = 0
        main_sla_countdown = 180

        mid_difficulty_marker = total_tickets / 2
        final_difficulty_marker = mid_difficulty_marker / 2

        ticket_presence = False
        caller_popup_window = None
        popup_button_accepted = False

        total_score = 0
        missed_calls = 0
        missed_tickets = 0
        current_ticket_id_index = 0
        
        title_image_path = "Assets/title.png"
        
        back_button = main_loop_elements.back_button_func(manager)
        title_label = main_loop_elements.title_image_func(manager, title_image_path)

        main_sla_timer_label = main_loop_elements.main_sla_timer_label_func(manager)
        caller_profile_tbox = main_loop_elements.caller_profile_tbox_func(manager)

        submit_button = main_loop_elements.submit_button_func(manager)
        threat_entry_title_tbox = main_loop_elements.threat_entry_title_tbox_func(manager)
        threat_entry_slist = main_loop_elements.threat_entry_slist_func(manager, threat_list)

        threat_panel, threat_title_tbox, threat_image, threat_description_tbox = main_loop_elements.threat_panel_func(manager)
        ticket_title_tbox = main_loop_elements.ticket_title_tbox_func(manager)
        ticket_entry_tbox = main_loop_elements.ticket_entry_tbox_func(manager)

        return start_shift_loop(connect, cursor, window_surface, clock, background, manager,
                               ticket_ids_list, total_tickets, threat_list, ticket_timer, 
                               randomized_ticket_entry, popup_window_close_timer, popup_window_sla_countdown,
                               main_sla_timer, main_sla_countdown, mid_difficulty_marker, final_difficulty_marker,
                               ticket_presence, caller_popup_window, popup_button_accepted,
                               total_score, missed_calls, missed_tickets, current_ticket_id_index, 
                               back_button, title_label, main_sla_timer_label, caller_profile_tbox, 
                               submit_button, threat_entry_title_tbox, threat_entry_slist,
                               threat_panel, threat_title_tbox, threat_image, threat_description_tbox,
                               ticket_title_tbox, ticket_entry_tbox)
    

    def start_shift_loop(connect, cursor, window_surface, clock, background, manager, 
                        ticket_ids_list, total_tickets, threat_list, ticket_timer, 
                        randomized_ticket_entry, popup_window_close_timer, popup_window_sla_countdown, 
                        main_sla_timer, main_sla_countdown, mid_difficulty_marker, final_difficulty_marker,
                        ticket_presence, caller_popup_window, popup_button_accepted, 
                        total_score, missed_calls, missed_tickets, current_ticket_id_index,  
                        back_button, title_label, main_sla_timer_label, caller_profile_tbox, 
                        submit_button, threat_entry_title_tbox, threat_entry_slist, 
                        threat_panel, threat_title_tbox, threat_image, threat_description_tbox, 
                        ticket_title_tbox, ticket_entry_tbox):

        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0
            ticket_timer += time_delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == threat_entry_slist:

                        selected_threat = event.text
                        print(selected_threat)

                        cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
                        description, indicators, countermeasures, image_path = cursor.fetchone()
                        threat_title_tbox.set_text(f'<b>{selected_threat.upper()}</b>')
                        threat_image_load = pygame.image.load(image_path)
                        threat_image.set_image(new_image=threat_image_load)
                        threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == back_button:
                        running = False
                    
                    if event.ui_element == submit_button and ticket_presence and selected_threat is not None:

                        ticket_title_tbox.set_text("")
                        ticket_entry_tbox.set_text("AWAITING TICKET...")
                        caller_profile_image.kill()
                        caller_profile_tbox.set_text("NO CALLER")
                        ticket_presence = False
                        ticket_timer = 0

                        main_sla_timer_label.set_text("SLA: ")

                        if selected_threat == answer:
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Correct")
                            total_score += 1
                        else:
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Wrong")
                        
                manager.process_events(event)
            
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))

            if ticket_timer >= randomized_ticket_entry and not ticket_presence and caller_popup_window is None:

                caller_popup_window, accept_button, popup_window_countdown = main_loop_elements.caller_popup_window_func(manager)
                popup_window_close_timer = 0

            if not ticket_ids_list and not ticket_presence:

                shift_report_init(window_surface, clock, background, manager,
                             total_score, total_tickets, missed_calls, missed_tickets)
                running = False
            
            else:

                if caller_popup_window:
                    caller_popup_window.show()
                    manager.draw_ui(window_surface)
                    popup_window_sla_countdown_difference = popup_window_sla_countdown - popup_window_close_timer

                    popup_window_countdown.set_text("SLA: {:.1f}".format(max(0, popup_window_sla_countdown_difference)))
                    popup_window_close_timer += time_delta

                    if popup_window_sla_countdown_difference <= 0:
                        caller_popup_window.hide()
                        caller_popup_window = None
                        selected_id = random.choice(ticket_ids_list)
                        ticket_ids_list.remove(selected_id)
                        ticket_timer = 0
                        missed_calls += 1

                    for event in pygame.event.get():
                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == accept_button:

                                main_sla_timer = 0

                                selected_id = ticket_ids_list[0]
                                cursor.execute('SELECT t.title, t.entry, t.answer, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?',
                                               [selected_id])
                                title, current_ticket, answer, caller_name, caller_org, caller_email, caller_contact, caller_picture = cursor.fetchone()
                                selected_threat = None

                                ticket_title_text = f"<b>ID#{selected_id} | {title}</b>"
                                ticket_title_tbox.set_text(ticket_title_text)

                                ticket_entry_tbox.set_text(current_ticket)
                                caller_profile_image = main_loop_elements.caller_profile_image_func(manager, caller_picture)

                                caller_profile_text = f"Name: {caller_name}\nOrganization: {caller_org}\nEmail: {caller_email}\nContact: {caller_contact}"
                                caller_profile_tbox.set_text(caller_profile_text)
                                
                                ticket_presence = True
                                ticket_ids_list.remove(selected_id)

                                caller_popup_window.hide()
                                caller_popup_window = None
                        
                        manager.process_events(event)

                else:
                    manager.draw_ui(window_surface)

                if len(ticket_ids_list) <= final_difficulty_marker:
                    main_sla_countdown = 60
                elif len(ticket_ids_list) <= mid_difficulty_marker:
                    main_sla_countdown = 120

                if ticket_presence and caller_popup_window is None:

                    main_sla_countdown_difference = main_sla_countdown - main_sla_timer
                    main_sla_timer_label.set_text("SLA: {:.1f}".format(max(0, main_sla_countdown_difference)))

                    main_sla_timer += time_delta

                    if main_sla_countdown_difference <= 0:
                        
                        ticket_title_tbox.set_text("")
                        ticket_entry_tbox.set_text("AWAITING TICKET...")
                        caller_profile_image.kill()
                        caller_profile_tbox.set_text("NO CALLER")
                        ticket_presence = False
                        ticket_timer = 0
                        missed_tickets += 1

                        main_sla_timer_label.set_text("SLA: ")

            manager.draw_ui(window_surface)
            pygame.display.update()


    def shift_report_init(window_surface, clock, background, manager, 
                          total_score, total_tickets, missed_calls, missed_tickets):
        
        assessment_percentage = (total_score / total_tickets) * 100
        if assessment_percentage >= 80:
            assessment_result = "PASS"
        else:
            assessment_result = "FAIL"
        
        manager.clear_and_reset()
        shift_report_tbox = main_loop_elements.shift_report_tbox_func(manager, total_score, total_tickets, 
                                                                      missed_calls, missed_tickets, 
                                                                      assessment_result)
        end_shift_title_label = main_loop_elements.end_shift_title_label_func(manager)
        end_shift_button = main_loop_elements.end_shift_button_func(manager)

        return shift_report(window_surface, clock, background, manager, 
                            shift_report_tbox, end_shift_title_label, end_shift_button, 
                            assessment_result)

    
    def shift_report(window_surface, clock, background, manager, 
                     shift_report_tbox, end_shift_title_label, end_shift_button, 
                     assessment_result):
        
        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == end_shift_button:
                        running = False

                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    start_shift_init(connect, cursor)