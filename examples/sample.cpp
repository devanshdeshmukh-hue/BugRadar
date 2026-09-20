#include <iostream>
using namespace std;

class Student
{
public:
    string name;
    int marks;
};

struct College
{
    string name;
    int students;
};
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
    // Get marks from user
    int marks;

    cout << "Enter marks: ";
    cin >> marks;

    int grade = calculateGrade(marks);

    cout << "Grade: " << grade;

    return 0;
}