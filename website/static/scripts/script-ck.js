$(document).ready(function(){if(document.location.search==="?fortwitter"){$(".instruct_button").hide();$(".leaderboard_link").hide()}$(".bingo_grid li").click(function(){console.log("click");$("#holder").fadeOut(100);var e=$(".bingo_grid").width();if(e<550){var t=$(this).clone();$("#holder").fadeIn(300);$("#holder li").remove();$("#holder").append(t)}});$(".close_box").click(function(){$("#holder").fadeOut(100)})});$("#instruct").click(function(){$("#body").addClass("no_scroll");$("#instruct_overlay").fadeIn(100);console.log("over")});$("#close_ins").click(function(){$("#body").removeClass("no_scroll");$("#instruct_overlay").fadeOut(100)});