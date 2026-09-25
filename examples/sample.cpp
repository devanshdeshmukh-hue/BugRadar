#include <iostream>
#include <vector>
#include <string>

using namespace std;


// ==========================================
// GRADE CALCULATION
// ==========================================

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


// ==========================================
// RECURSIVE FUNCTION
// ==========================================

int factorial(int n)
{
    if (n <= 1)
    {
        return 1;
    }

    return n * factorial(n - 1);
}


// ==========================================
// DATA PROCESSING
// ==========================================

int processData(
    int a,
    int b,
    int limit
)
{
    int result = 0;

    for (int i = 0; i < limit; i++)
    {
        if (a > 10 && b > 10)
        {
            result += i;
        }
        else if (a > 5 || b > 5)
        {
            result += 2;
        }
        else
        {
            result += 1;
        }
    }

    while (result < 100)
    {
        result++;
    }

    return result;
}


// ==========================================
// MAIN FUNCTION
// ==========================================

int main()
{
    int marks;

    cout << "Enter marks: ";
    cin >> marks;

    int grade = calculateGrade(marks);

    int result = (marks >= 40) ? 1 : 0;

    int factorialResult = factorial(5);

    int processed = processData(
        marks,
        grade,
        5
    );


    // ======================================
    // SWITCH TEST
    // ======================================

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
    cout << "Factorial: " << factorialResult;
    cout << "Processed: " << processed;

    return 0;
}