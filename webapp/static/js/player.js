//ADD YOUR CODE HERE.


$(document).ready(function () {
     data = {
        "steps": [{
                        "id": "1",
                        "content": "tip on first div",
                        "selector": "#id_1",
                        "next": "2"
                },{
                        "id": "2",
                        "content": "tip on second div",
                        "selector": ".myClass2",
                        "next": "3",
                },{
                        "id": "3",
                        "content": "tip on third div.",
                        "selector": "div:eq(2)",
                        "next": null,
                }]
     }
       
     $.each(data.steps, function(key, val) {
           $(val.selector).hover(function(){
              $(this).attr('title', val.content).tooltip();
           });
     })
});
