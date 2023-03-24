function init()
{
    setInterval(updatePressureGauges, 1000);
}

function valveCheckboxHandler(checkbox)
{
    const valveButtonName = checkbox.name;
    const valveButtonState = checkbox.checked;

    $.getJSON('/valve_toggle/'+valveButtonName,
                function(data) {
              console.log(data);
            });    
}

function updatePressureGauges()
{
    const gauge1 = $("#gauge1");
    const gauge2 = $("#gauge2");

    $.getJSON('/pressure_data',
                function(data) {
              gauge1.attr("data-value", data.P1);
              gauge2.attr("data-value", data.P2);
            });
}