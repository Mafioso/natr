$(document).ready(function() {
	"use strict";
	
	
	
	
	
	
	
	
	
	
	//fit text
	function fit_text(element, lenght) {
		var text = $.trim($(element).html());
		text = text.substr(0, lenght) + "...";
		
		$(element).html(text);
	}
	
	
	
	
	
	
	
	
	
	
	//body
	//close blocks if mouse clicked outside of them
	$(document).mouseup(function(e) {
		//close chat
		var chat_button_container = $(".head .tools .control .chat");
    	var chat_window_container = $(".block_chat");

    	if ((!chat_window_container.is(e.target)) && ((chat_button_container.has(e.target).length === 0) && (chat_window_container.has(e.target).length === 0))) {
        	$(".head .tools .control .chat").removeClass("active");
			$(".block_chat").stop().animate({"opacity": "0.0"}, 200, chat_fade);
			
			chat_open = false;
    	}
		
		
		//close user settings menu
		var user_settings_container = $(".head .tools .control .user_setup");
		
		if ((!user_settings_container.is(e.target)) && (user_settings_container.has(e.target).length === 0)) {
        	user_settings_menu_hide();
    	}
	});
	
	
	
	
	
	
	
	
	
	
	//head
	//user settings
	var head_user_setting_open = false;
	
	$(".head .tools .control .user_setup").on("click", function() {
		if (head_user_setting_open === false) {
			user_settings_menu_show();
		} else {
			user_settings_menu_hide();
		}
	});
	
	function user_settings_menu_show() {
		head_user_setting_open = true;
		
		$(".head .tools .control .user_setup").addClass("active");
		
		$(".head .tools .control .user_settings_menu").css("display", "block");
		$(".head .tools .control .user_settings_menu").css("opacity", "0.0");
		$(".head .tools .control .user_settings_menu").stop().animate({"opacity": "1.0", "top": "79px"}, 500, "easeInOutQuart");
	}
	
	function user_settings_menu_hide() {
		head_user_setting_open = false;
		
		$(".head .tools .control .user_setup").removeClass("active");
		
		$(".head .tools .control .user_settings_menu").stop().animate({"opacity": "0.0", "top": "69px"}, 200, "easeInOutQuart", user_settings_menu_fade);
		
		function user_settings_menu_fade() {
			$(".head .tools .control .user_settings_menu").css("display", "none");
		}
	}
	
	
	
	
	
	
	
	
	
	
	//dashboard
	//fit text in tasks widget
	$(".widget_tasks .widget_items").children().each(function(index, element) {
        fit_text($(element).children().eq(0).children().eq(0), 40);
    });
	
	//fit chat project name
	$(".block_chat .chat_box .contacts .list").children().each(function(index, element) {
		fit_text($(element).children().eq(1), 20);
    });
	
	
	
	
	
	
	
	
	
	
	//reports
	//fit projects list names
	$(".reports .reports_projects .projects .box_projects").children().each(function(index, element) {
        fit_text($(element).children().eq(0).children().eq(0), 30);
		fit_text($(element).children().eq(0).children().eq(1), 46);
    });
	
	
	
	
	
	
	
	
	
	
	//journal
	//fit projects list names
	function fit_journal_projects() {
		$(".journal .journal_projects .projects .box_projects").children().each(function(index, element) {
			fit_text($(element).children().eq(0).children().eq(0), 30);
			fit_text($(element).children().eq(0).children().eq(1), 46);
		});
	}
	
	fit_journal_projects();
	
	//fit journal item fields
	function fit_journal_item_fields() {
	$(".block_journal_table .titles .fields").children().each(function(index, element) {
		//alert($.trim($(element).children().eq(0).html()).length);
		//alert(Math.round(parseInt($(element).children().eq(0).css("width")) / 8));
		
		if ($.trim($(element).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).css("width")) / 8) - 2)) {
			fit_text($(element).children().eq(0), (Math.round(parseInt($(element).children().eq(0).css("width")) / 8) - 2));
		}
		
		
		//if (int($(element).children().eq(0).css("width")) > )
        //fit_text($(element).children().eq(0), 6);
    });
	
	$(".block_journal_table .items").children().each(function(index, element) {
		//alert(Math.round(parseInt($(element).children().eq(0).children().eq(0).css("width")) / 8));
		//alert($.trim($(element).children().eq(0).children().eq(0).children().eq(0).html()).length);
		
		if ($.trim($(element).children().eq(0).children().eq(0).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).children().eq(0).css("width")) / 8) - 1)) {
			fit_text($(element).children().eq(0).children().eq(0).children().eq(0), (Math.round(parseInt($(element).children().eq(0).children().eq(0).css("width")) / 8) - 1));
		}
		if ($.trim($(element).children().eq(0).children().eq(1).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).children().eq(1).css("width")) / 8) - 2)) {
			fit_text($(element).children().eq(0).children().eq(1).children().eq(0), (Math.round(parseInt($(element).children().eq(0).children().eq(1).css("width")) / 8) - 2));
		}
		if ($.trim($(element).children().eq(0).children().eq(2).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).children().eq(2).css("width")) / 8) - 4)) {
			fit_text($(element).children().eq(0).children().eq(2).children().eq(0), (Math.round(parseInt($(element).children().eq(0).children().eq(2).css("width")) / 8) - 4));
		}
		if ($.trim($(element).children().eq(0).children().eq(3).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).children().eq(3).css("width")) / 8) - 3)) {
			fit_text($(element).children().eq(0).children().eq(3).children().eq(0), (Math.round(parseInt($(element).children().eq(0).children().eq(3).css("width")) / 8) - 3));
		}
		if ($.trim($(element).children().eq(0).children().eq(4).children().eq(0).html()).length > (Math.round(parseInt($(element).children().eq(0).children().eq(4).css("width")) / 8) - 4)) {
			fit_text($(element).children().eq(0).children().eq(4).children().eq(0), (Math.round(parseInt($(element).children().eq(0).children().eq(4).css("width")) / 8) - 4));
		}
		
        //fit_text($(element).children().eq(0).children().eq(2).children().eq(0), 6);
		//fit_text($(element).children().eq(0).children().eq(3).children().eq(0), 6);
		//fit_text($(element).children().eq(0).children().eq(4).children().eq(0), 6);
    });
	}
	
	fit_journal_item_fields();
	
	
	
	
	
	
	
	
	
	
	//project
	function project_resize_steps_menu() {
		$(".block_project_step_info .steps .step").css("width", (($(".block_project_step_info .steps").width() / $(".block_project_step_info .steps .step").length ) - 1) + "px");
	}
	
	project_resize_steps_menu();
	
	
	
	
	
	
	
	
	
	
	//project - edit
	function project_edit_set_page(page) {
		$(".project_edit .project_edit_body").children().each(function(index, element) {
			$(element).css("display", "none");
		});
		
		$(".project_edit .project_edit_body").children().eq(page).css("display", "block");
	}
	
	function project_edit_set_menu(menu_item) {
		$(".project_edit .project_edit_menu .items").children().each(function(index, element) {
			$(element).removeClass("active");
		});
		
		$(".project_edit .project_edit_menu .items").children().each(function(index, element) {
			if (index === menu_item)  {
				$(element).addClass("active");
			}
		});
	}
	
	project_edit_set_page(0);
	project_edit_set_menu(0);
	
	
	
	
	
	//menu reactions
	$(".project_edit_menu .items .item").on("click", function() {
		/*$(".project_edit_menu .items").children().each(function(index, element) {
			$(element).removeClass("active");
		});
		
		$(this).addClass("active");*/
		
		project_edit_set_menu($(this).index());
		project_edit_set_page($(this).index());
	});
	
	
	
	
	
	//page next reactions
	//main data
	$(".project_edit .main_data .next_button").on("click", function() {
		project_edit_set_menu(1);
		project_edit_set_page(1);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	//project calendar plan
	$(".project_edit .project_calendar_plan .next_button").on("click", function() {
		project_edit_set_menu(2);
		project_edit_set_page(2);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	//costing
	$(".project_edit .costings .next_button").on("click", function() {
		project_edit_set_menu(3);
		project_edit_set_page(3);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	//costing explanation
	$(".project_edit .costings_explanation .next_button").on("click", function() {
		project_edit_set_menu(4);
		project_edit_set_page(4);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	//project efficiency data
	$(".project_edit .project_efficiency_data .next_button").on("click", function() {
		project_edit_set_menu(5);
		project_edit_set_page(5);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	//project passport
	$(".project_edit .project_passport .next_button").on("click", function() {
		project_edit_set_menu(6);
		project_edit_set_page(6);
		
		$("html, body").stop().animate({"scrollTop": "0"}, 500, "easeInOutQuart");
	});
	
	
	
	
	
	//founders table
	//add new line
	$(".project_edit .main_data .button_add").on("click", function() {
		var temp_line = $(".project_edit .main_data .block_founders_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".project_edit .main_data .block_founders_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".project_edit .main_data .block_founders_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".project_edit .main_data .block_founders_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	//project team table
	//add new line
	$(".project_edit .monitoring_plan .block_project_team_table .button_add").on("click", function() {
		var temp_line = $(".project_edit .monitoring_plan .block_project_team_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".project_edit .monitoring_plan .block_project_team_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".project_edit .monitoring_plan .block_project_team_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".project_edit .monitoring_plan .block_project_team_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	//calendar plan table
	//add new line
	$(".project_edit .project_calendar_plan .block_calendar_plan_table .button_add").on("click", function() {
		var temp_line = $(".project_edit .project_calendar_plan .block_calendar_plan_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".project_edit .project_calendar_plan .block_calendar_plan_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".project_edit .project_calendar_plan .block_calendar_plan_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".project_edit .project_calendar_plan .block_calendar_plan_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	//calendar plan fact table
	//add new line
	$(".project_edit .project_calendar_plan .block_calendar_plan_fact_table .button_add").on("click", function() {
		var temp_line = $(".project_edit .project_calendar_plan .block_calendar_plan_fact_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".project_edit .project_calendar_plan .block_calendar_plan_fact_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".project_edit .project_calendar_plan .block_calendar_plan_fact_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".project_edit .project_calendar_plan .block_calendar_plan_fact_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	//monitoring plan table
	//add new line
	$(".project_edit .monitoring_plan .block_monitoring_plan_table .button_add").on("click", function() {
		var temp_line = $(".project_edit .monitoring_plan .block_monitoring_plan_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".project_edit .monitoring_plan .block_monitoring_plan_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".project_edit .monitoring_plan .block_monitoring_plan_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".project_edit .monitoring_plan .block_monitoring_plan_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	//gp report second table
	//add new line
	$(".report .report_body .block_report_second_table .button_add").on("click", function() {
		var temp_line = $(".report .report_body .block_report_second_table .items").children().eq(0).clone();
		
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(1).find(".input_text input").val("");
		$(temp_line).children().eq(0).children().eq(2).find(".input_text input").val("");
		
		$(".report .report_body .block_report_second_table .items").append(temp_line);
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").focus();
		$(temp_line).children().eq(0).children().eq(0).find(".input_text input").parent().addClass("focus");
		
		$(temp_line).find(".input_text input").focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(temp_line).find(".input_text input").blur(function() {
			$(this).parent().removeClass("focus");
		});
	});
	
	//delete line
	$(".report .report_body .block_report_second_table .items").on("click", ".delete", function() {
		var list_size = parseInt($(".report .report_body .block_report_second_table .items").children().size());
		
		if (list_size > 1) {
			$(this).parent().remove();
		} 
	});
	
	
	
	
	
	
	
	
	
	
	
	//chat
	var chat_open = false;
	
	
	
	//turn chat on and off
	$(".head .tools .control .chat").on("click", function() {
		if (chat_open === false) {
			$(this).addClass("active");
			$(".block_chat").css("display", "block");
			$(".block_chat").css("opacity", "0.0");
			$(".block_chat .chat_box .messages").scrollTop($(".block_chat .chat_box .messages")[0].scrollHeight);
			$(".block_chat").stop().animate({"opacity": "1.0"}, 200);
			//$(".block_chat .chat_box .messages").stop().delay(200).animate({scrollTop: $(".block_chat .chat_box .messages").prop("scrollHeight")}, 1000);
			
			chat_open = true;
		} else {
			$(this).removeClass("active");
			$(".block_chat").stop().animate({"opacity": "0.0"}, 200, chat_fade);
			
			chat_open = false;
		}
	});
	
	function chat_fade() {
		$(".block_chat").css("display", "none");
	}
	
	
	
	//prevent page scroll when mouse over chat
	$(".block_chat .chat_box .messages, .block_chat .chat_box .contacts").on("mousewheel DOMMouseScroll", function (e) {
    	var original_delta = e.originalEvent;
		var delta = original_delta.wheelDelta || -original_delta.detail;
    	
    	this.scrollTop += (delta < 0 ? 1 : -1) * 40;
		
    	if (!e) {
        	e = window.event;
    	}
		
    	if (e.preventDefault) {
        	e.preventDefault();
    	}
		
    	e.returnValue = false;
	});
	
	
	
	//add message to chat
	$(".block_chat .tools_box .send").on("click", function() {
		chat_add_message();
	});
	
	$(".block_chat .tools_box .message").on("keypress", function(e) {
        if (e.keyCode === 13) {
            chat_add_message();
			
            return false;
        }
	});
	
	function chat_add_message() {
		var date = new Date();
		
		var month = date.getMonth() + 1;
		if (month < 10) {
			month = "0" + month;
		}
		
		var day = date.getDate();
		if (day < 10) {
			day = "0" + day;
		}
		
		var now_date = day + "." + month + "." + date.getFullYear() + " / " + date.getHours() + ":" + date.getMinutes();
		
		if ($(".block_chat .tools_box .message input").val() !== "") {
			$(".block_chat .chat_box .messages .list").append('<div class="message_right"><div class="date">' + now_date + '</div><div class="text">' + $(".block_chat .tools_box .message input").val() + '</div><div class="arrow"><svg viewBox="0 0 26 15" style="background-color:#ffffff00" x="0px" y="0px" width="26px" height="15px"><path class="svg_chat_right_arrow_icon" d="M 23 3.5069 L 23 11.6897 C 23 14.9177 21.2092 15.9644 19 14.0276 L 4.96 1.7184 C 4.6733 1.5315 4.3511 1.3426 4 1.169 C 1.605 -0.0155 0 0 0 0 L 26 0 C 26 0 24.7813 0.0365 24 1.169 C 23.0254 2.5817 23 3.5069 23 3.5069 Z" fill="#e3ecf2"/></svg></div><div class="cleaner"></div></div>');
			//$(".block_chat .chat_box .messages").scrollTop($(".block_chat .chat_box .messages")[0].scrollHeight);
			$(".block_chat .chat_box .messages").stop().animate({scrollTop: $(".block_chat .chat_box .messages").prop("scrollHeight")}, 1000, "easeInOutQuart");
			$(".block_chat .tools_box .message input").val("");
		}
	}
	
	
	
	
	
	
	
	
	
	
	
	//scroll
	$(window).on("scroll", function() {
		//position main menu and chat
		if ($(window).scrollTop() > 100) {
			$(".main_menu").css("top", "50px");
			$(".block_chat").css("top", "0");
		} else {
			$(".main_menu").css("top", (150 - ($(window).scrollTop())));
			$(".block_chat").css("top", (100 - ($(window).scrollTop())));
		}
		
		
		
		
		
		//position project edit menu
		if ($(window).scrollTop() < 100) {
			$(".project_edit_menu .items").css("top", "0");
		} else {
			$(".project_edit_menu .items").css("top", ((0 + ($(window).scrollTop())) - 100));
		}
	});
	
	
	
	
	
	
	
	
	
	
	//resize
	$(window).resize(function() {
    	fit_journal_projects();
		fit_journal_item_fields();
		
		project_resize_steps_menu();
	});

	
	
	
	
	
	
	
	
	
	
	//outline all inputs
	//$(".project_edit .project_calendar_plan .block_calendar_plan_table .items").on("click", ".delete", function() {
	$(".input_text").each(function(index, element) {
        $(element).find(".wrap").children().eq(0).focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(element).find(".wrap").children().eq(0).blur(function() {
			$(this).parent().removeClass("focus");
		});
    });
	
	
	
	$(".input_textarea").each(function(index, element) {
        $(element).find(".wrap").children().eq(0).focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(element).find(".wrap").children().eq(0).blur(function() {
			$(this).parent().removeClass("focus");
		});
    });
	
	
	
	$(".select_text").each(function(index, element) {
        $(element).find(".wrap").children().eq(0).focus(function() {
			$(this).parent().addClass("focus");
		});
		
		$(element).find(".wrap").children().eq(0).blur(function() {
			$(this).parent().removeClass("focus");
		});
    });
	
	
	
	/*$(".input_text").children().eq(0).children().eq(0).focus(function() {
		$(this).parent().addClass("focus");
	});
	
	$(".input_text").children().eq(0).children().eq(0).blur(function() {
		$(this).parent().removeClass("focus");
	});*/
});
















