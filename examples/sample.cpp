#include <iostream>
using namespace std;

// Function to calculate grade
int calculateGrade(int marks)
{
    if (marks >= 90)
    {
        return 1;
    }
    else if (marks >= 80)
    {
        return 2;
    }
    else if (marks >= 70)
    {
        return 3;
    }
    else
    {
        return 4;
    }
}

int main()
{
    int marks;

    cout << "Enter marks: ";
    cin >> marks;

    int grade = calculateGrade(marks);

    // Test ternary operator
    int result = (marks >= 40) ? 1 : 0;

    // Test switch statement
    switch (grade)
    {
        case 1:
            cout << "Excellent";
            break;

        case 2:
            cout << "Very Good";
            break;

        case 3:
            cout << "Good";
            break;

        default:
            cout << "Needs Improvement";
            break;
    }

    cout << "Grade: " << grade;
    cout << "Result: " << result;

    return 0;
}