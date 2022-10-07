/* Name: Keiser Dallas
 * Class: CSC 403-002
 * Date: 10/06/2022
 * Desc: This is a C# example of a decorator pattern being used a simple car class.
 * The program dynamically expands object functionalities without making changes
 * to the abstract class. After instantiation, the regular car is given additional
 * features not listed in the abstract car class. 
 */


using System;
using System.Runtime.InteropServices;


namespace DecoratorPatternExample
{

    // Create a base interface w/ a general method
    interface ICar
    {
        // Create a function to get car description
        string getCarModel();
    }


    // Create a concrete implementation
    //   (Inherits from ICar interface)
    class Car : ICar
    {
        // Create a general car description
        public string getCarModel()
        {
            return ("This is car is a ");
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
            car = newCar;

        }

        // Create a car description
        public virtual string getCarModel()
        {
            return (car.getCarModel());
        }

    }




    // Create multiple concrete decorators that take a car as input and add additional features
    //  (Additional functionalities)

    // Give the car a make and model
    class MakeModel : CarCustomizer 
    {
        public MakeModel(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            string feature = base.getCarModel();
            feature += (" Tesla Model Y. Features include:  ");
            return feature;
        }
    }


    // Add a sunroof
    class AddSunroof : CarCustomizer
    {
        public AddSunroof(ICar newCar) : base(newCar) { }

        public override string getCarModel()
        {
            string feature = base.getCarModel();
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
            string feature = base.getCarModel();
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
            string feature = base.getCarModel();
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
            string feature = base.getCarModel();
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
            ICar tesla = new MakeModel(car);

            // Add a sunroof
            ICar sunroof = new AddSunroof(tesla);

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
