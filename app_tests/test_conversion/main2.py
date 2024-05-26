from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Load the kv file
Builder.load_file('medi_metrics.kv')

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ("%w/v", "mg/mL"): 10,
        ("%w/v", "g/L"): 10,
        ("%w/v", "ppm"): 10000,  # Added conversion for %w/v to ppm
        ("%w/w", "ppm"): 10000,
        ("ppm", "mg/L"): 1,
        ("mg/mL", "g/L"): 1,
        ("g/L", "mg/mL"): 1000,
        ("mg/L", "ppm"): 1,
        ("mM", "M"): 0.001,
        ("M", "mM"): 1000,
        ("mg", "g"): 0.001,
        ("g", "mg"): 1000,
        ("g", "kg"): 0.001,
        ("kg", "g"): 1000,
        ("mL", "L"): 0.001,
        ("L", "mL"): 1000,
        ("µL", "mL"): 0.001,
        ("mL", "µL"): 1000,
    }

    if (from_unit, to_unit) in conversion_factors:
        return value * conversion_factors[(from_unit, to_unit)]
    elif (to_unit, from_unit) in conversion_factors:
        return value / conversion_factors[(to_unit, from_unit)]
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")

class RootWidget(BoxLayout):
    input_value = ObjectProperty(None)
    from_unit = ObjectProperty(None)
    to_unit = ObjectProperty(None)
    result_label = ObjectProperty(None)

    def calculate_conversion(self):
        try:
            # Retrieve and convert the input value
            input_value = self.ids.input_value.text
            from_unit = self.ids.from_unit.text
            to_unit = self.ids.to_unit.text
            value = float(input_value)

            if from_unit.startswith("Select") or to_unit.startswith("Select"):
                raise ValueError("Please select both units.")

            # Perform the unit conversion
            result = convert_units(value, from_unit, to_unit)
            self.ids.result_label.text = f"Result: {result:.4f} {to_unit}"
        except ValueError as e:
            # Display error messages in a popup
            popup = Popup(
                title="Error",
                content=Label(text=str(e)),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

class MediMetricsApp(App):
    def build(self):
        # Set the title of the app
        self.title = "MediMetrics"
        return RootWidget()

if __name__ == "__main__":
    MediMetricsApp().run()
