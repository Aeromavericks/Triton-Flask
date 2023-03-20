function valveCheckboxHandler(checkbox)
{
    const valveButtonName = checkbox.name;
    const valveButtonState = checkbox.checked;

    $.getJSON('/valve_toggle/'+valveButtonName,
                function(data) {
              console.log(data);
            });

    updatePressureGauges();
    
}

function updatePressureGauges()
{
    const element = $("#gauge1");
    $.getJSON('/pressure_data',
                function(data) {
              element.attr("data-value", data.P1)
            });
}