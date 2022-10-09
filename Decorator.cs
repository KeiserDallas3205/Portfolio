/* Name: Keiser Dallas
 * Class: CSC 403-002
 * Date: 10/06/2022
 * Desc: This is an example of a decorator pattern being used a simple car class.
 * The program dynamically expands object functionalities without making changes
 * to the abstract class. After instantiation, the regular car is given a make, model,
 * and additional features not listed in the abstract car class. 
 */


using System;
using System.Runtime.InteropServices;


namespace DecoratorPatternExample
{

    // Create a base interface w/ a general method
    interface ICar
    {
        // Create a function to generate a car description
        string getCarModel();
    }


    // Create a concrete implementation
    //   (Inherits from ICar interface)
    class Car : ICar
    {
        // Create a general car description
        public string getCarModel()
        {
            return ("This car is a ");
        }
    }


    // Create a base decorator that takes a car as input and customizes it 
    //     (Inherits from ICar interface)
    class CarCustomizer : ICar
    {
        // Create a car type
        private ICar car;

        public CarCustomizer(ICar newCar)
        {
            // Save the current car's info into a car that can be customized
            car = newCar;

        }

        // Update the car's description
        public virtual string getCarModel()
        {
            // Return the customized car's description
            return (car.getCarModel());
        }

    }




    // Create multiple concrete decorators that take a car as input and add additional features
    //  (Additional functionalities)

    // Give the user a make and model of their choice 
    class MakeModel : CarCustomizer 
    {
        public MakeModel(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            // Get car's current description
            string feature = base.getCarModel();
            
            // Prompt user for their choice of car
            Console.WriteLine("What kind of car would you like to purchase?");

            // Store user response
            string typeOfCar = Console.ReadLine();
            
            // Update car's description
            feature += (typeOfCar + (". Features include:  "));
            return feature;
        }
    }


    // Add a sunroof
    class AddSunroof : CarCustomizer
    {
        public AddSunroof(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            // Get car's current description
            string feature = base.getCarModel();

            // Update car's description
            feature += ("\r\n a sunroof");
            return feature;
        }

    }


    // Add a underglow lights
    class AddUnderglow : CarCustomizer
    {
        public AddUnderglow(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            // Get car's current description
            string feature = base.getCarModel();

            // Update car's description
            feature += ("\r\n underglow lights");
            return feature;
        }

    }

    // Add bluetooth
    class AddBluetooth : CarCustomizer
    {

        public AddBluetooth(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            // Get car's currrent description
            string feature = base.getCarModel();

            // Update car's description
            feature += ("\r\n bluetooth");
            return feature;
        }
    }

    // Add self-driving technology
    class SelfDriving : CarCustomizer 
    {
        public SelfDriving(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            // Get car's current description
            string feature = base.getCarModel();

            // Update car's description
            feature += ("\r\n fully self-driving capabilities");
            return feature;
        }
    }


    // ************ MAIN ****************  
    class Program
    {
        static void Main(string[] args)
        {
            // Decorator Design Pattern Example

            // Create a new car
            ICar car = new Car();

            // Give it a make and model
            ICar typeOfCar = new MakeModel(car);

            // Add a sunroof
            ICar sunroof = new AddSunroof(typeOfCar);

            // Add underglow lights
            ICar lights = new AddUnderglow(sunroof);

            // Add bluetooth 
            ICar bluetooth = new AddBluetooth(lights);

            // Add self-driving capabilities
            ICar autopilot = new SelfDriving(bluetooth);

            // Print the car's make, model, and features
            Console.WriteLine(autopilot.getCarModel());
        }
    }

}
