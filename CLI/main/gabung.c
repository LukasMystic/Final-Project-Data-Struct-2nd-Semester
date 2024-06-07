#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
//===================================================================================
 void mainDatasiswa();
//TREE LOGIN REGISTER
// Structure for a teacher node
struct Teacher {
    char codeGuru[100];
    char fullname[100];
    char email[100];
};

// AVL tree1 node
struct AVLNode {
    struct Teacher *teacher;
    int height;
    struct AVLNode *left;
    struct AVLNode *right;
};

// Function to create a new teacher node
struct Teacher* createTeacher(char codeGuru[], char fullname[], char email[]) {
    struct Teacher *newTeacher = (struct Teacher*)malloc(sizeof(struct Teacher));
    strcpy(newTeacher->codeGuru, codeGuru);
    strcpy(newTeacher->fullname, fullname);
    strcpy(newTeacher->email, email);
    return newTeacher;
}

// Function to get the maximum of two integers
int max1(int a, int b) {
    return (a > b) ? a : b;
}

// Function to get the height of a node
int height(struct AVLNode *node) {
    if (node == NULL)
        return 0;
    return node->height;
}

// Function to perform a left rotation
struct AVLNode* rotateLeft(struct AVLNode *y) {
    struct AVLNode *x = y->right;
    struct AVLNode *T2 = x->left;

    x->left = y;
    y->right = T2;

    // Update heights
    y->height = max1(height(y->left), height(y->right)) + 1;
    x->height = max1(height(x->left), height(x->right)) + 1;

    return x;
}

// Function to perform a right rotation
struct AVLNode* rotateRight(struct AVLNode *x) {
    struct AVLNode *y = x->left;
    struct AVLNode *T2 = y->right;

    y->right = x;
    x->left = T2;

    // Update heights
    x->height = max1(height(x->left), height(x->right)) + 1;
    y->height = max1(height(y->left), height(y->right)) + 1;

    return y;
}

// Function to get the balance factor of a node
int getBalance(struct AVLNode *node) {
    if (node == NULL)
        return 0;
    return height(node->left) - height(node->right);
}

// Function to insert a teacher into AVL tree
struct AVLNode* insertTeacherAVL(struct AVLNode *root, struct Teacher *teacher) {
    if (root == NULL) {
        struct AVLNode *newNode = (struct AVLNode*)malloc(sizeof(struct AVLNode));
        newNode->teacher = teacher;
        newNode->height = 1;
        newNode->left = NULL;
        newNode->right = NULL;
        return newNode;
    }

    int compare;
    if (root->teacher == NULL) {
        compare = -1; // Assume the teacher's codeGuru is smaller than any non-NULL value
    } else {
        compare = strcmp(teacher->codeGuru, root->teacher->codeGuru);
    }

    if (compare < 0)
        root->left = insertTeacherAVL(root->left, teacher);
    else if (compare > 0)
        root->right = insertTeacherAVL(root->right, teacher);
    else {
        free(teacher);
        return root;
    }

    // Update height
    root->height = 1 + max1(height(root->left), height(root->right));
    int balance = getBalance(root);

    // LLC
    if (balance > 1 && (root->left != NULL) && strcmp(teacher->codeGuru, root->left->teacher->codeGuru) < 0)
        return rotateRight(root);

    // RRC
    if (balance < -1 && (root->right != NULL) && strcmp(teacher->codeGuru, root->right->teacher->codeGuru) > 0)
        return rotateLeft(root);

    // LRC
    if (balance > 1 && (root->left != NULL) && strcmp(teacher->codeGuru, root->left->teacher->codeGuru) > 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    // RLC
    if (balance < -1 && (root->right != NULL) && strcmp(teacher->codeGuru, root->right->teacher->codeGuru) < 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    return root;
}


// Function to search for a teacher by name
struct Teacher* search(struct AVLNode *root, char codeGuru[]) {
    if (root == NULL || strcmp(root->teacher->codeGuru, codeGuru) == 0)
        return root ? root->teacher : NULL;

    if (strcmp(codeGuru, root->teacher->codeGuru) < 0)
        return search(root->left, codeGuru);
    else
        return search(root->right, codeGuru);
}

struct Teacher* searchfullname(struct AVLNode *root, char fullname[]) {
    if (root == NULL || strcmp(root->teacher->fullname, fullname) == 0)
        return root ? root->teacher : NULL;

    if (strcmp(fullname, root->teacher->fullname) < 0)
        return search(root->left, fullname);
    else
        return search(root->right, fullname);
}

struct AVLNode* loadTeachersFromFile(struct AVLNode *root, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Error: Could not open file %s\n", filename);
        return root;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        char *fullname = strtok(line, ",");
        char *codeGuru = strtok(NULL, ",");
        char *email = strtok(NULL, "\n");

        if (fullname && codeGuru && email) {
            struct Teacher *newTeacher = createTeacher(codeGuru, fullname, email);
            root = insertTeacherAVL(root, newTeacher);
        }
    }

    fclose(file);
    return root;
}
struct Teacher* searchByEmail(struct AVLNode *root, char email[]) {
    if (root == NULL) return NULL;

    if (strcmp(root->teacher->email, email) == 0) {
        return root->teacher;
    }

    struct Teacher *result = searchByEmail(root->left, email);
    if (result != NULL) return result;

    return searchByEmail(root->right, email);
}
// Function to search for a teacher by codeGuru
struct Teacher* search3(struct AVLNode *root, char codeGuru[]) {
    if (root == NULL || strcmp(root->teacher->codeGuru, codeGuru) == 0)
        return root ? root->teacher : NULL;

    if (strcmp(codeGuru, root->teacher->codeGuru) < 0)
        return search3(root->left, codeGuru);
    else
        return search3(root->right, codeGuru);
}

//===================================================================================
// AVL TREE 2
//TREE DATA SISWA
// Structure for a data siswa

// Structure for a student
struct DataSiswa {
    char studentID[100];
    char fullname[100];
    int nilaiMat;
    int nilaiFis;
    int nilaiKim;
    int nilaiBio;
    int nilaiBindo;
    int kelas;
};

// AVL tree node
struct AVLSiswa {
    struct DataSiswa *data;
    int height2;
    struct AVLSiswa *left;
    struct AVLSiswa *right;
};

void IDgenerator(){

}
// Function to create a new student node
struct DataSiswa* createDataSiswa(char fullname[], int nilaiMat, int nilaiFis, int nilaiKim, int nilaiBio, int nilaiBindo, int kelas) {
    struct DataSiswa *newSiswa = (struct DataSiswa*)malloc(sizeof(struct DataSiswa));
    strcpy(newSiswa->fullname, fullname);
    newSiswa->nilaiMat = nilaiMat;
    newSiswa->nilaiFis = nilaiFis;
    newSiswa->nilaiKim = nilaiKim;
    newSiswa->nilaiBio = nilaiBio;
    newSiswa->nilaiBindo = nilaiBindo;
    newSiswa->kelas = kelas;
    return newSiswa;
}

// Function to get the maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Function to get the height2 of a node
int height2(struct AVLSiswa *node) {
    if (node == NULL)
        return 0;
    return node->height2;
}

// Function to perform a left rotation
struct AVLSiswa* rotateLeft2(struct AVLSiswa *y) {
    struct AVLSiswa *x = y->right;
    struct AVLSiswa *T2 = x->left;

    x->left = y;
    y->right = T2;

    // Update 
    y->height2 = max(height2(y->left), height2(y->right)) + 1;
    x->height2 = max(height2(x->left), height2(x->right)) + 1;

    return x;
}

// Function to get the balance factor of a node
int getBalance2(struct AVLSiswa *node) {
    if (node == NULL)
        return 0;
    return height2(node->left) - height2(node->right);
}

// Function to perform a right rotation
struct AVLSiswa* rotateRight2(struct AVLSiswa *x) {
    struct AVLSiswa *y = x->left;
    struct AVLSiswa *T2 = y->right;

    y->right = x;
    x->left = T2;

    // Update 
    x->height2 = max(height2(x->left), height2(x->right)) + 1;
    y->height2 = max(height2(y->left), height2(y->right)) + 1;

    return y;
}

// Function to insert a student into AVL tree
struct AVLSiswa* insertDataSiswa(struct AVLSiswa *node, struct DataSiswa *data) {
    if (node == NULL) {
        struct AVLSiswa *newNode = (struct AVLSiswa*)malloc(sizeof(struct AVLSiswa));
        newNode->data = data;
        newNode->height2 = 1;
        newNode->left = NULL;
        newNode->right = NULL;
        return newNode;
    }

    int compare = strcmp(data->fullname, node->data->fullname);

    if (compare < 0)
        node->left = insertDataSiswa(node->left, data);
    else if (compare > 0)
        node->right = insertDataSiswa(node->right, data);
    else {
        printf("Fullname must be unique!\n");
        return node;
    }

    // Update height2 
    node->height2 = 1 + max(height2(node->left), height2(node->right));
    int balance = getBalance2(node);

    // LLC
    if (balance > 1 && strcmp(data->fullname, node->left->data->fullname) < 0)
        return rotateRight2(node);

    // RRC
    if (balance < -1 && strcmp(data->fullname, node->right->data->fullname) > 0)
        return rotateLeft2(node);

    // LRC
    if (balance > 1 && strcmp(data->fullname, node->left->data->fullname) > 0) {
        node->left = rotateLeft2(node->left);
        return rotateRight2(node);
    }

    // RLC
    if (balance < -1 && strcmp(data->fullname, node->right->data->fullname) < 0) {
        node->right = rotateRight2(node->right);
        return rotateLeft2(node);
    }

    return node;
}

// Function to search22 for a student by fullname
struct AVLSiswa* search2(struct AVLSiswa *root, char *fullname) {
    if (root == NULL || strcmp(root->data->fullname, fullname) == 0)
        return root;

    if (strcmp(fullname, root->data->fullname) < 0)
        return search2(root->left, fullname);
    else
        return search2(root->right, fullname);
}

// Function to find the node with the minimum value
struct AVLSiswa* minValueNode(struct AVLSiswa *node) {
    struct AVLSiswa *current = node;

    while (current && current->left != NULL)
        current = current->left;

    return current;
}

// Function to delete a student node
struct AVLSiswa* deleteDataSiswa(struct AVLSiswa *node, char *fullname) {
    if (node == NULL)
        return node;

    if (strcmp(fullname, node->data->fullname) < 0)
        node->left = deleteDataSiswa(node->left, fullname);
    else if (strcmp(fullname, node->data->fullname) > 0)
        node->right = deleteDataSiswa(node->right, fullname);
    else {
        if (node->left == NULL) {
            struct AVLSiswa *temp = node->right;
            free(node);
            return temp;
        } else if (node->right == NULL) {
            struct AVLSiswa *temp = node->left;
            free(node);
            return temp;
        }

        struct AVLSiswa *temp = minValueNode(node->right);
        node->data = temp->data;
        node->right = deleteDataSiswa(node->right, temp->data->fullname);
    }

    // Update 
    node->height2 = 1 + max(height2(node->left), height2(node->right));
    int balance = getBalance2(node);

    // LLC
    if (balance > 1 && getBalance2(node->left) >= 0)
        return rotateRight2(node);

    // LRC
    if (balance > 1 && getBalance2(node->left) < 0) {
        node->left = rotateLeft2(node->left);
        return rotateRight2(node);
    }

    // RRC
    if (balance < -1 && getBalance2(node->right) <= 0)
        return rotateLeft2(node);

    // RLC
    if (balance < -1 && getBalance2(node->right) > 0) {
        node->right = rotateRight2(node->right);
        return rotateLeft2(node);
    }

    return node;
}



//root2

//----------------------------------------FUNCTION SELAIN AVL TREE----------------------------------------------------------

//---------------------------------------------LOGIN/REGISTER---------------------------------------------------------------
// Function to clear the screen
void ClearScreen() {
    printf("Press enter to continue...");
    getchar();
    system("cls"); // Clear the screen
}

void appendTeacherToFile(const char *filename, struct Teacher *teacher) {
    FILE *file = fopen(filename, "a");
    if (!file) {
        printf("Error: Could not open file %s\n", filename);
        return;
    }

    fprintf(file, "%s,%s,%s\n", teacher->fullname, teacher->codeGuru, teacher->email);
    fclose(file);
}

void generateVerificationCode() {
    FILE *fp;
    int i, code[10];

    // Seed the random number generator
    srand(time(NULL));

    // Generate a random 10-digit code
    for (i = 0; i < 10; i++) {
        code[i] = rand() % 10;
    }

    // Open the file in write mode, overwriting it if it already exists
    fp = fopen("verif.csv", "w");
    if (fp == NULL) {
        printf("Unable to open file.\n");
        return;
    }

    // Write the code to the file
    for (i = 0; i < 10; i++) {
        fprintf(fp, "%d", code[i]);
    }

    // Close the file
    fclose(fp);

    printf("Verification code generated and written to verif.csv.\n");
}

// Function to verify the code entered by the user
int verifyCode(char *code) {
    FILE *fp;
    char storedCode[11];
    struct AVLNode *root = NULL;
    root = loadTeachersFromFile(root, "DataGuru.csv");

    // Open the file for reading
    fp = fopen("verif.csv", "r");
    if (fp == NULL) {
        printf("Verification file not found.\n");
        return 0;
    }

    // Read the stored code from the file
    fscanf(fp, "%s", storedCode);

    // Close the file
    fclose(fp);

    // Compare the entered code with the stored code
    if (strcmp(code, storedCode) == 0) {
        return 1;
    } else {
        return 0;
    }
}

// Function to display login page
void loginPage() {
    struct AVLNode *root = NULL;
    root = loadTeachersFromFile(root, "DataGuru.csv");

    while (1) {
        printf("Login Page\n");
        printf("===========\n\n");
        char codeGuru[100];
        char fullname[100];
        printf("Enter your Teacher ID: ");
        scanf("%s", codeGuru);
        printf("Enter your fullname: ");
        scanf("%s", fullname);

        struct Teacher *result = search(root, codeGuru);
        if (result != NULL && strcmp(result->codeGuru, codeGuru) == 0 && strcmp(result->fullname, fullname) == 0) {
            

            // Generate and display verification code
            generateVerificationCode();
            printf("Please enter the verification code: ");
            char verificationCode[11];
            scanf("%s", verificationCode);

            // Verify the code
            if (verifyCode(verificationCode)) {
			    printf("Verification successful!\n");
			    printf("Login successful! Welcome, %s.\n", result->fullname);
			    printf("\nGo to Our Homepage System ==>\n");
			    getchar(); // Clear remaining input buffer
			    ClearScreen();
			    
			    mainDatasiswa();
			    return;
			} else {
			    printf("Verification failed! Incorrect code.\n");
			    printf("Press [1] to go back to login page.\n");
			    int choice;
			    scanf("%d", &choice);
			
			    // Clear input buffer
			    while (getchar() != '\n');
			
			    ClearScreen();
			    if (choice == 1) {
			        continue;
			    }
			}

        } else {
            printf("Login failed! Check your ID or fullname. Please try again.\n");
            printf("Press [1] to go back or [2] to retry: ");
            int choice;
            scanf("%d", &choice);

            // Clear input buffer
            while (getchar() != '\n');

            ClearScreen();
            if (choice == 1) {
                return;
            }
        }
    }
}


// For registration
void registerPage(struct AVLNode **root) {
    // Load teachers from file before registration
    *root = loadTeachersFromFile(*root, "DataGuru.csv");

    printf("Register Page\n");
    printf("==============\n\n");

    char codeGuru[100];
    char fullname[100];
    char email[100];

    // Input email
    printf("Enter your email: ");
    scanf("%s", email);

	// Validate email format
	int emailLength = strlen(email);
	if (emailLength < 6 || strchr(email, '@') == NULL) {
	    int comIndex = emailLength - 4;
	    int idIndex = emailLength - 3;
	    if ((comIndex < 0 || strncmp(&email[comIndex], ".com", 4) != 0) &&
	        (idIndex < 0 || strncmp(&email[idIndex], ".id", 3) != 0)) {
	        printf("Invalid email format! Email must contain '@' symbol and end with '.com' or '.id'.\n");
	        getchar(); // Clear remaining input buffer
	        ClearScreen();
	        return;
	    }
	}




    // Check if email already exists
    struct Teacher *emailCheck = searchByEmail(*root, email);
    if (emailCheck != NULL) {
        printf("User with this email already exists. Please use another email.\n");
        getchar(); // Clear remaining input buffer
        ClearScreen();
        return;
    }

    // Input Teacher ID
    printf("Enter your Teacher ID (10 digits): ");
    scanf("%s", codeGuru);
    
    // Validate Teacher ID format
    int codeGuruLength = strlen(codeGuru);
    if (codeGuruLength != 10 || !isdigit(codeGuru[0])) {
        printf("Invalid Teacher ID format! Teacher ID must have exactly 10 digits.\n");
        getchar(); // Clear remaining input buffer
        ClearScreen();
        return;
    }

    // Check if Teacher ID already exists
    struct Teacher *result = search(*root, codeGuru);
    if (result != NULL) {
        printf("User with this ID already exists. Please choose another ID.\n");
        getchar(); // Clear remaining input buffer
        ClearScreen();
        return;
    }

    // Input fullname
    printf("Enter your fullname: ");
    scanf("%s", fullname);

    // Create new teacher and insert into AVL tree
    struct Teacher *newTeacher = createTeacher(codeGuru, fullname, email);
    *root = insertTeacherAVL(*root, newTeacher);
    // Append new teacher to file
    appendTeacherToFile("DataGuru.csv", newTeacher);

    printf("Registration successful! Please login to continue.\n");
    getchar(); // Clear remaining input buffer
    ClearScreen();
    loginPage(*root);
}



//---------------------------------------------DATA SISWA---------------------------------------------------------------

// void insertData(struct AVLSiswa **node) {
//     char title[26];
//     char genre[20];
//     int stock;
//     char fullname[100];
//     int nilaiMat, nilaiFis, nilaiKim, nilaiBio, nilaiBindo, kelas;

//     while (1) {
//         printf("Input fullname[5-90]: ");
//         fgets(fullname, sizeof(fullname), stdin);
//         fullname[strcspn(fullname, "\n")] = '\0'; 
//         if (strlen(fullname) < 5 || strlen(fullname) > 90) {
//             printf("Fullname must be between 5 and 90 characters!\n");
//             continue;
//         }

//         if (search(*node, fullname) != NULL) {
//             printf("Fullname must be unique!\n");
//             continue;
//         }
//         break;
//     }

//     while (1) {
//         printf("Input game genre[Action|RPG|Adventure|Card Game]: ");
//         fgets(genre, sizeof(genre), stdin);
//         genre[strcspn(genre, "\n")] = '\0'; 
//         if (strcmp(genre, "Action") != 0 && strcmp(genre, "RPG") != 0 &&
//             strcmp(genre, "Adventure") != 0 && strcmp(genre, "Card Game") != 0) {
//             printf("Invalid game genre! Please enter Action, RPG, Adventure, or Card Game.\n");
//             continue;
//         }

//         break;
//     }

//     while (1) {
//         printf("Input game stock[>= 1]: ");
//         scanf("%d", &stock);
//         if (stock < 1) {
//             printf("Game stock must be at least 1!\n");
//             continue;
//         }
//         getchar(); 
//         break;
//     }

//     struct Game *newGame = createGameNode(fullname, genre, stock);
//     *node = insertGameAVL(*node, newGame);

//     printf("Insert success!\n");
//     ClearScreen();
// }
// Function to print a row of the table
// void printTableRow(char studentID[],char fullname[], int nilaiMat, int nilaiFis, int nilaiKim, int nilaiBio, int nilaiBindo, int kelas) {
//     printf("| %-25s | %-25s | %-9d | %-9d | %-9d | %-9d | %-9d | %-9d |\n", studentID, fullname, nilaiMat, nilaiFis, nilaiKim, nilaiBio, nilaiBindo, kelas);
//     printf("---------------------------------------------------------\n");
// }



// In-Order Traversal 
// void inorderTraversal(struct AVLNode *root) {
//     if (root != NULL) {
//         inorderTraversal(root->left);
//         printTableRow(root->game->title, root->game->genre, root->game->stock);
//         inorderTraversal(root->right);
//     }
   
// }

// Function to display all games using In-Order traversal
// void displayGames(struct AVLNode **root) {
//     if (*root == NULL) {
//         printf("Warehouse is empty!\n\n");
//         ClearScreen();
//         return;// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
//     }

//     printf("---------------------------------------------------------\n");
//     printf("| %-25s | %-12s | %-10s |\n", "Game Title", "Game Genre", "Game Stock");
//     printf("---------------------------------------------------------\n");
//     inorderTraversal(*root);
//     printf("\n");
// 	ClearScreen();
// }


//----------------------------------------------------------------------------------------------------------------
//-------------------------------------------MAIN FUNCTION--------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------
 void mainDatasiswa(){
    int choice;
    do {
        struct AVLSiswa *node = NULL;
        system("cls");
        printf(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n");
        printf("|                    Welcome To Homepage                        |\n");
        printf("|                                                               |\n");
        printf("|             HIGH SCHOOL TEACHER ASSESSMENT SYSTEM             |\n");
        printf(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n");
        printf("|                                                               |\n");
        printf("|           Tools Menu for Assessment:                          |\n");
        printf("|                                                               |\n");

        // Print menu options using a for loop
        char* options[] = {
            "|    1. Insert Student Information and Grades                   |",
            "|    2. Sort, View, and Export Student Grades                   |",
            "|    3. Edit Student Information and Grades                     |",
            "|    4. Delete Student Data                                     |",
            "|    5. Export Grades (Unsorted)                                |",
            "|    6. Close the Program                                       |"
        };

        for (int i = 0; i < 6; i++) {
            printf("%s\n", options[i]);
        }

        printf("|                                                               |\n");
        printf("/////////////////////////////////////////////////////////////////\n");
        // printf("\n");
        printf("|\n");
        printf(" ===> Choose an Option from the Tools Menu [1-6]: ");
        scanf("%d", &choice);
        // Clear input buffer
        while (getchar() != '\n');
		system("cls");

        switch (choice) {
            case 1:
                //insertData(&node);
                break;
            case 2:
                //displayStudents(&node);
                break;
            case 3:
                //updateStudent(&node);
                break;
            case 4:
                //deleteStudent(&node);
                break;
            case 5:
                //exportData(&node);
            case 6:
                printf("Exiting...\n");
                exit(0);
            default:
                printf("Invalid choice! Please enter a number between 1 and 5.\n\n");
                ClearScreen();
        }

    } while (choice != 6);
    return;
 }

// Main function
int main() {
    struct AVLNode *root = NULL;
    int choice;
    do {
        printf("Login & Register Page\n");
	    printf("======================\n");
        printf("\n1. Login\n2. Register\n3. Exit\nEnter your choice: ");
        scanf("%d", &choice);

        // Clear input buffer
        while (getchar() != '\n');
		system("cls");

        switch (choice) {
            case 1:
                loginPage(root);
                
                break;
            case 2:
                registerPage(&root);
                break;
            case 3:
                printf("Exiting...\n");
                exit(0);
            default:
                printf("Invalid choice. Please enter again.\n");
                ClearScreen();
        }
    } while (choice != 3);

    return 0;
}
