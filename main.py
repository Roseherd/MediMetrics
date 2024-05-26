from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup


# Function to convert between different units based on given conversion factors
def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ('%w/v', 'mg/mL'): 10,
        ('%w/v', 'g/L'): 10,
        ('%w/v', 'ppm'): 10000,
        ('%w/w', 'ppm'): 10000,
        ('ppm', 'mg/L'): 1,
        ('mg/mL', 'g/L'): 1,
        ('g/L', 'mg/mL'): 1000,
        ('mg/L', 'ppm'): 1,
        ('mM', 'M'): 0.001,
        ('M', 'mM'): 1000,
        ('mg', 'g'): 0.001,
        ('g', 'mg'): 1000,
        ('g', 'kg'): 0.001,
        ('kg', 'g'): 1000,
        ('mL', 'L'): 0.001,
        ('L', 'mL'): 1000,
        ('µL', 'mL'): 0.001,
        ('mL', 'µL'): 1000
    }

    if (from_unit, to_unit) in conversion_factors:
        return value * conversion_factors[(from_unit, to_unit)]
    elif (to_unit, from_unit) in conversion_factors:
        return value / conversion_factors[(to_unit, from_unit)]
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")


# Main application class inheriting from Kivy's App class
class MediMetricsApp(App):
    def build(self):
        # Set the title of the app
        self.title = "MediMetrics - Pharmaceutical Calculations"

        # Create the main layout (vertical box layout)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for the value to convert
        self.input_value = TextInput(hint_text="Enter value", multiline=False, input_filter='float')
        layout.add_widget(self.input_value)

        # Dropdown (Spinner) for selecting the 'from' unit
        self.from_unit = Spinner(
            text="Select 'From' Unit",
            values=("%w/v", "mg/mL", "g/L", "%w/w", "ppm", "mM", "M", "mg", "g", "kg", "mL", "L", "µL"),
        )
        layout.add_widget(self.from_unit)

        # Dropdown (Spinner) for selecting the 'to' unit
        self.to_unit = Spinner(
            text="Select 'To' Unit",
            values=("mg/mL", "g/L", "%w/v", "%w/w", "ppm", "mM", "M", "mg", "g", "kg", "mL", "L", "µL"),
        )
        layout.add_widget(self.to_unit)

        # Label to display the result of the conversion
        self.result_label = Label(text="Result: ")
        layout.add_widget(self.result_label)

        # Button to trigger the conversion calculation
        convert_button = Button(text="Convert", on_press=self.calculate_conversion)
        layout.add_widget(convert_button)

        return layout

    def calculate_conversion(self, instance):
        try:
            # Retrieve and convert the input value
            value = float(self.input_value.text)
            from_unit = self.from_unit.text
            to_unit = self.to_unit.text
            if from_unit.startswith("Select") or to_unit.startswith("Select"):
                raise ValueError("Please select both units.")

            # Perform the unit conversion
            result = convert_units(value, from_unit, to_unit)
            self.result_label.text = f"Result: {result:.4f} {to_unit}"
        except ValueError as e:
            # Display error messages in a popup
            popup = Popup(title='Error',
                          content=Label(text=str(e)),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


# Entry point of the application
if __name__ == "__main__":
    MediMetricsApp().run()
