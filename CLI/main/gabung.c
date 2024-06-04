#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
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

    int compare = strcmp(teacher->codeGuru, root->teacher->codeGuru);

    if (compare < 0)
        root->left = insertTeacherAVL(root->left, teacher);
    else if (compare > 0)
        root->right = insertTeacherAVL(root->right, teacher);
    else {
        printf("Teacher name must be unique!\n");
        return root;
    }

    // Update height
    root->height = 1 + max1(height(root->left), height(root->right));
    int balance = getBalance(root);

    // LLC
    if (balance > 1 && strcmp(teacher->codeGuru, root->left->teacher->codeGuru) < 0)
        return rotateRight(root);

    // RRC
    if (balance < -1 && strcmp(teacher->codeGuru, root->right->teacher->codeGuru) > 0)
        return rotateLeft(root);

    // LRC
    if (balance > 1 && strcmp(teacher->codeGuru, root->left->teacher->codeGuru) > 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    // RLC
    if (balance < -1 && strcmp(teacher->codeGuru, root->right->teacher->codeGuru) < 0) {
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

//===================================================================================
//TREE DATA SISWA
// Structure for a data siswa

// Structure for a student
struct DataSiswa {
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
    int height;
    struct AVLSiswa *left;
    struct AVLSiswa *right;
};

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

// Function to get the height of a node
int height(struct AVLSiswa *node) {
    if (node == NULL)
        return 0;
    return node->height;
}

// Function to perform a left rotation
struct AVLSiswa* rotateLeft(struct AVLSiswa *y) {
    struct AVLSiswa *x = y->right;
    struct AVLSiswa *T2 = x->left;

    x->left = y;
    y->right = T2;

    // Update 
    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    return x;
}

// Function to get the balance factor of a node
int getBalance(struct AVLSiswa *node) {
    if (node == NULL)
        return 0;
    return height(node->left) - height(node->right);
}

// Function to perform a right rotation
struct AVLSiswa* rotateRight(struct AVLSiswa *x) {
    struct AVLSiswa *y = x->left;
    struct AVLSiswa *T2 = y->right;

    y->right = x;
    x->left = T2;

    // Update 
    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    return y;
}

// Function to insert a student into AVL tree
struct AVLSiswa* insertDataSiswa(struct AVLSiswa *node, struct DataSiswa *data) {
    if (node == NULL) {
        struct AVLSiswa *newNode = (struct AVLSiswa*)malloc(sizeof(struct AVLSiswa));
        newNode->data = data;
        newNode->height = 1;
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

    // Update height 
    node->height = 1 + max(height(node->left), height(node->right));
    int balance = getBalance(node);

    // LLC
    if (balance > 1 && strcmp(data->fullname, node->left->data->fullname) < 0)
        return rotateRight(node);

    // RRC
    if (balance < -1 && strcmp(data->fullname, node->right->data->fullname) > 0)
        return rotateLeft(node);

    // LRC
    if (balance > 1 && strcmp(data->fullname, node->left->data->fullname) > 0) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }

    // RLC
    if (balance < -1 && strcmp(data->fullname, node->right->data->fullname) < 0) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
    }

    return node;
}

// Function to search for a student by fullname
struct AVLSiswa* search(struct AVLSiswa *root, char *fullname) {
    if (root == NULL || strcmp(root->data->fullname, fullname) == 0)
        return root;

    if (strcmp(fullname, root->data->fullname) < 0)
        return search(root->left, fullname);
    else
        return search(root->right, fullname);
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
    node->height = 1 + max(height(node->left), height(node->right));
    int balance = getBalance(node);

    // LLC
    if (balance > 1 && getBalance(node->left) >= 0)
        return rotateRight(node);

    // LRC
    if (balance > 1 && getBalance(node->left) < 0) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }

    // RRC
    if (balance < -1 && getBalance(node->right) <= 0)
        return rotateLeft(node);

    // RLC
    if (balance < -1 && getBalance(node->right) > 0) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
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

// Function to display login page
void loginPage(struct AVLNode *root) {
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
        printf("Login successful! Welcome, %s.\n", result->fullname);
        printf("\nGo to Our Homepage System ==>\n");
        getchar();
        ClearScreen();
        mainDatasiswa();
    } else {
        printf("Login failed check your ID or fullname!\nPlease try again.\n");
        printf("Press [1] to back: ");
        int choice;
        scanf("%d", &choice);

        // Clear input buffer
        while (getchar() != '\n');
		system("cls");

        switch (choice) {
            case 1:
                return;
                break;
            default:
                printf("Okay continue to login. Please enter again\n");
                ClearScreen();
                loginPage(root);
                break;
        }
    }
}

// Function to display register page
void registerPage(struct AVLNode **root) {
    printf("Register Page\n");
	printf("==============\n\n");
    char codeGuru[100];
    char fullname[100];
    char email[100];
    printf("Enter your email: ");
    scanf("%s", email);

    printf("Enter your Teacher ID: ");
    scanf("%s", codeGuru);
    struct Teacher *result = search(*root, codeGuru);
    if (result != NULL) {
        printf("User with this name already exists. Please choose another name.\n");
        ClearScreen();
        registerPage(root);
    } else {
        printf("Enter your fullname: ");
        scanf("%s", fullname);
        struct Teacher *newTeacher = createTeacher(codeGuru, fullname, email);
        *root = insertTeacherAVL(*root, newTeacher);
        printf("Registration successful! Please login to continue.\n");
        ClearScreen();
        loginPage(*root);
    }
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


//----------------------------------------------------------------------------------------------------------------
//-------------------------------------------MAIN FUNCTION--------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------
 void mainDatasiswa(){
//     int choice;
//     struct AVLSiswa *node = NULL;
//     do {
//         printf("Student Data Management\n");
//         printf("========================\n");
//         printf("1. Insert Student\n");
//         printf("2. View Students\n");
//         printf("3. Update Student\n");
//         printf("4. Delete Student\n");
//         printf("5. Exit\n");
//         printf(">> ");

//         scanf("%d", &choice);
//         // Clear input buffer
//         while (getchar() != '\n');
// 		system("cls");

//         switch (choice) {
//             case 1:
//                 insertData(&node);
//                 break;
//             case 2:
//                 displayStudents(&node);
//                 break;
//             case 3:
//                 updateStudent(&node);
//                 break;
//             case 4:
//                 deleteStudent(&node);
//                 break;
//             case 5:
//                 printf("Exiting...\n");
//                 exit(0);
//             default:
//                 printf("Invalid choice! Please enter a number between 1 and 5.\n\n");
//                 ClearScreen();
//         }
//     } while (choice != 5);
    int choice;
    
    do {
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
        

    } while (choice < 1 || choice > 6);

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
