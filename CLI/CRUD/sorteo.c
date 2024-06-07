#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Struct
typedef struct {
    char name[50];
    float nilai_matematika;
    float nilai_fisika;
    float nilai_kimia;
    float nilai_biologi;
    float nilai_bahasa_indonesia;
    char kelas[10];
} Student;

// AscendDescend
int compareNameAsc(const void *a, const void *b) {
    return strcmp(((Student *)a)->name, ((Student *)b)->name);
}

int compareNameDesc(const void *a, const void *b) {
    return strcmp(((Student *)b)->name, ((Student *)a)->name);
}

int compareMathAsc(const void *a, const void *b) {
    float diff = ((Student *)a)->nilai_matematika - ((Student *)b)->nilai_matematika;
    return (diff > 0) - (diff < 0);
}

int compareMathDesc(const void *a, const void *b) {
    float diff = ((Student *)b)->nilai_matematika - ((Student *)a)->nilai_matematika;
    return (diff > 0) - (diff < 0);
}

int comparePhysicsAsc(const void *a, const void *b) {
    float diff = ((Student *)a)->nilai_fisika - ((Student *)b)->nilai_fisika;
    return (diff > 0) - (diff < 0);
}

int comparePhysicsDesc(const void *a, const void *b) {
    float diff = ((Student *)b)->nilai_fisika - ((Student *)a)->nilai_fisika;
    return (diff > 0) - (diff < 0);
}

int compareChemistryAsc(const void *a, const void *b) {
    float diff = ((Student *)a)->nilai_kimia - ((Student *)b)->nilai_kimia;
    return (diff > 0) - (diff < 0);
}

int compareChemistryDesc(const void *a, const void *b) {
    float diff = ((Student *)b)->nilai_kimia - ((Student *)a)->nilai_kimia;
    return (diff > 0) - (diff < 0);
}

int compareBiologyAsc(const void *a, const void *b) {
    float diff = ((Student *)a)->nilai_biologi - ((Student *)b)->nilai_biologi;
    return (diff > 0) - (diff < 0);
}

int compareBiologyDesc(const void *a, const void *b) {
    float diff = ((Student *)b)->nilai_biologi - ((Student *)a)->nilai_biologi;
    return (diff > 0) - (diff < 0);
}

int compareIndonesianAsc(const void *a, const void *b) {
    float diff = ((Student *)a)->nilai_bahasa_indonesia - ((Student *)b)->nilai_bahasa_indonesia;
    return (diff > 0) - (diff < 0);
}

int compareIndonesianDesc(const void *a, const void *b) {
    float diff = ((Student *)b)->nilai_bahasa_indonesia - ((Student *)a)->nilai_bahasa_indonesia;
    return (diff > 0) - (diff < 0);
}

int compareClassAsc(const void *a, const void *b) {
    return strcmp(((Student *)a)->kelas, ((Student *)b)->kelas);
}

int compareClassDesc(const void *a, const void *b) {
    return strcmp(((Student *)b)->kelas, ((Student *)a)->kelas);
}

// Sort
void sortStudents(Student students[], int count, int field, int order) {
    switch(field) {
        case 1: // Name
            if (order == 0)
                qsort(students, count, sizeof(Student), compareNameAsc);
            else
                qsort(students, count, sizeof(Student), compareNameDesc);
            break;
        case 2: // Math
            if (order == 0)
                qsort(students, count, sizeof(Student), compareMathAsc);
            else
                qsort(students, count, sizeof(Student), compareMathDesc);
            break;
        case 3: // Physics
            if (order == 0)
                qsort(students, count, sizeof(Student), comparePhysicsAsc);
            else
                qsort(students, count, sizeof(Student), comparePhysicsDesc);
            break;
        case 4: // Chemistry
            if (order == 0)
                qsort(students, count, sizeof(Student), compareChemistryAsc);
            else
                qsort(students, count, sizeof(Student), compareChemistryDesc);
            break;
        case 5: // Biology
            if (order == 0)
                qsort(students, count, sizeof(Student), compareBiologyAsc);
            else
                qsort(students, count, sizeof(Student), compareBiologyDesc);
            break;
        case 6: // Indonesian
            if (order == 0)
                qsort(students, count, sizeof(Student), compareIndonesianAsc);
            else
                qsort(students, count, sizeof(Student), compareIndonesianDesc);
            break;
        case 7: // Class
            if (order == 0)
                qsort(students, count, sizeof(Student), compareClassAsc);
            else
                qsort(students, count, sizeof(Student), compareClassDesc);
            break;
        default:
            printf("Invalid field\n");
    }
}

// Read CSV
int readStudentsFromCSV(const char *filename, Student students[], int max_count) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        return 0;
    }

    char line[256];
    int count = 0;

    // Ignore header
    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file);
        return 0; // Return 0 if file is empty
    }

    while (fgets(line, sizeof(line), file) && count < max_count) {
        sscanf(line, "%49[^,],%f,%f,%f,%f,%f,%9[^\n]",
               students[count].name, &students[count].nilai_matematika, &students[count].nilai_fisika,
               &students[count].nilai_kimia, &students[count].nilai_biologi, 
               &students[count].nilai_bahasa_indonesia, students[count].kelas);
        count++;
    }

    fclose(file);
    return count;
}

// Valid
int isValidNumber(char *input) {
    for (int i = 0; input[i] != '\0'; i++) {
        if (!isdigit(input[i])) {
            return 0;
        }
    }
    return 1;
}

/*
int main() {
    Student students[100];
    int count;
    int field, order;
    char input[10];

    // Read students from CSV file
    count = readStudentsFromCSV("students.csv", students, 100);

    if (count == 0) {
        printf("No students read from file or file not found.\n");
        return 1;
    }

    // Get sorting preferences from user
    do {
        printf("Choose the field to sort by:\n");
        printf("1. Name\n");
        printf("2. Math Grade\n");
        printf("3. Physics Grade\n");
        printf("4. Chemistry Grade\n");
        printf("5. Biology Grade\n");
        printf("6. Indonesian Grade\n");
        printf("7. Class\n");
        printf("Enter the field number: ");
        scanf("%s", input);

        if (isValidNumber(input)) {
            field = atoi(input);
            if (field < 1 || field > 7) {
                printf("Error: Invalid field number. Please enter a number between 1 and 7.\n");
            }
        } else {
            printf("Error: Invalid input. Please enter a valid number.\n");
            field = -1; // Set an invalid value to repeat the loop
        }
    } while (field < 1 || field > 7);

    do {
        printf("Choose the sorting order:\n");
        printf("0. Ascending\n");
        printf("1. Descending\n");
        printf("Enter the sorting order: ");
        scanf("%s", input);

        if (isValidNumber(input)) {
            order = atoi(input);
            if (order != 0 && order != 1) {
                printf("Error: Invalid sorting order. Please enter 0 for Ascending or 1 for Descending.\n");
            }
        } else {
            printf("Error: Invalid input. Please enter a valid number.\n");
            order = -1; // Set an invalid value to repeat the loop
        }
    } while (order != 0 && order != 1);

    // Sort students based on user input
    sortStudents(students, count, field, order);

    // Export the sorted data into an array of structs
    Student sortedStudents[count];
    for (int i = 0; i < count; i++) {
        sortedStudents[i] = students[i];
    }

    // Print sorted students to verify
    printf("\nSorted Students:\n");
    for (int i = 0; i < count; i++) {
        printf("%s, %.2f, %.2f, %.2f, %.2f, %.2f, %s\n",
               sortedStudents[i].name, sortedStudents[i].nilai_matematika, sortedStudents[i].nilai_fisika,
               sortedStudents[i].nilai_kimia, sortedStudents[i].nilai_biologi, 
               sortedStudents[i].nilai_bahasa_indonesia, sortedStudents[i].kelas);
    }

    return 0;
}*/
