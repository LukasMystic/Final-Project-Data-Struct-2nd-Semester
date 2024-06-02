// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


// ------------------------------------------- AVL TREE ------------------------------------------------------------//

// Structure for a game node
struct Game {
    char title[26];
    char genre[20];
    int stock;
    struct Game *left;
    struct Game *right;
};

// AVL tree node
struct AVLNode {
    struct Game *game;
    int height;
    struct AVLNode *left;
    struct AVLNode *right;
};

// Function to create a new game node
struct Game* createGameNode(char title[], char genre[], int stock) {
    struct Game *newGame = (struct Game*)malloc(sizeof(struct Game));
    strcpy(newGame->title, title);// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
    strcpy(newGame->genre, genre);
    newGame->stock = stock;
    newGame->left = NULL;
    newGame->right = NULL;
    return newGame;
}
// Function to get the maximum of two integers
int max(int a, int b) {
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

    // Update 
    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    return x;
}
// Function to get the balance factor of a node
int getBalance(struct AVLNode *node) {
    if (node == NULL)
        return 0;
    return height(node->left) - height(node->right);// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
}

// Function to perform a right rotation
struct AVLNode* rotateRight(struct AVLNode *x) {
    struct AVLNode *y = x->left;
    struct AVLNode *T2 = y->right;

    y->right = x;
    x->left = T2;

    // Update 
    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    return y;
}


// Function to insert a game into AVL tree
struct AVLNode* insertGameAVL(struct AVLNode *root, struct Game *game) {
    if (root == NULL) {
        struct AVLNode *newNode = (struct AVLNode*)malloc(sizeof(struct AVLNode));
        newNode->game = game;
        newNode->height = 1;
        newNode->left = NULL;
        newNode->right = NULL;
        return newNode;
    }

    int compare = strcmp(game->title, root->game->title);

    if (compare < 0)
        root->left = insertGameAVL(root->left, game);
    else if (compare > 0)
        root->right = insertGameAVL(root->right, game);
    else {
        printf("Game title must be unique!\n");
        return root;
    }

    // Update height 
    root->height = 1 + max(height(root->left), height(root->right));
    int balance = getBalance(root);

    // LLC
    if (balance > 1 && strcmp(game->title, root->left->game->title) < 0)
        return rotateRight(root);

    // RRC
    if (balance < -1 && strcmp(game->title, root->right->game->title) > 0)
        return rotateLeft(root);// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566

    // LRC
    if (balance > 1 && strcmp(game->title, root->left->game->title) > 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    // RLC
    if (balance < -1 && strcmp(game->title, root->right->game->title) < 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    return root;
}

// Function to search for a game by title 
struct Game* search(struct AVLNode *root, char title[]) {
    if (root == NULL || strcmp(root->game->title, title) == 0)
        return root ? root->game : NULL;

    if (strcmp(title, root->game->title) < 0)
        return search(root->left, title);
    else
        return search(root->right, title);
}

// Function to find the node with the minimum value 
struct AVLNode* minValueNode(struct AVLNode *node) {
    struct AVLNode *current = node;

    while (current && current->left != NULL)
        current = current->left;

    return current;
}

// Function to delete a game node 
struct AVLNode* deleteGame(struct AVLNode *root, char title[]) {
    if (root == NULL) {
        return root;
    }

    if (strcmp(title, root->game->title) < 0) {
        root->left = deleteGame(root->left, title);
    }
    
    else if (strcmp(title, root->game->title) > 0) {
        root->right = deleteGame(root->right, title);
    }
    else {
        // Node with only one child or no child
        if (root->left == NULL) {
            struct AVLNode *temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            struct AVLNode *temp = root->left;
            free(root);
            return temp;
        }

        // Node with two children (smallest in the right subtree)
        struct AVLNode *temp = minValueNode(root->right);

        // Copy the inorder successor's content to this node
        strcpy(root->game->title, temp->game->title);
        strcpy(root->game->genre, temp->game->genre);
        root->game->stock = temp->game->stock;

        // Delete
        root->right = deleteGame(root->right, temp->game->title);
    }

    // Update 
    root->height = 1 + max(height(root->left), height(root->right));// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566

    int balance = getBalance(root);

    // LLC
    if (balance > 1 && getBalance(root->left) >= 0)
        return rotateRight(root);

    // LRC
    if (balance > 1 && getBalance(root->left) < 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    // RRC
    if (balance < -1 && getBalance(root->right) <= 0)
        return rotateLeft(root);

    // RLC
    if (balance < -1 && getBalance(root->right) > 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    return root;
}

// --------------------------------------------------- END ----------------------------------------------------//


// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
// Function to clear the screen
void ClearScreen() {
    printf("Press enter to continue...\n");
    getchar();
    system("cls"); // Clear the screen
}

// Function to insert a game
void insertGame(struct AVLNode **root) {
    char title[26];
    char genre[20];
    int stock;

    while (1) {
        printf("Input game title[5-25][unique]: ");
        fgets(title, sizeof(title), stdin);
        title[strcspn(title, "\n")] = '\0'; 
        if (strlen(title) < 5 || strlen(title) > 25) {
            printf("Game title must be between 5 and 25 characters!\n");
            continue;
        }

        if (search(*root, title) != NULL) {
            printf("Game title must be unique!\n");
            continue;
        }
// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
        break;
    }

    while (1) {
        printf("Input game genre[Action|RPG|Adventure|Card Game]: ");
        fgets(genre, sizeof(genre), stdin);
        genre[strcspn(genre, "\n")] = '\0'; 
        if (strcmp(genre, "Action") != 0 && strcmp(genre, "RPG") != 0 &&
            strcmp(genre, "Adventure") != 0 && strcmp(genre, "Card Game") != 0) {
            printf("Invalid game genre! Please enter Action, RPG, Adventure, or Card Game.\n");
            continue;
        }

        break;
    }

    while (1) {
        printf("Input game stock[>= 1]: ");
        scanf("%d", &stock);
        if (stock < 1) {
            printf("Game stock must be at least 1!\n");
            continue;
        }
        getchar(); 
        break;
    }

    struct Game *newGame = createGameNode(title, genre, stock);
    *root = insertGameAVL(*root, newGame);

    printf("Insert success!\n");
    ClearScreen();
}


// Function to print a row of the table
void printTableRow(char title[], char genre[], int stock) {
    printf("| %-25s | %-12s | %-10d |\n", title, genre, stock);
    printf("---------------------------------------------------------\n");
}


// In-Order Traversal 
void inorderTraversal(struct AVLNode *root) {
    if (root != NULL) {
        inorderTraversal(root->left);
        printTableRow(root->game->title, root->game->genre, root->game->stock);
        inorderTraversal(root->right);
    }
   
}


// Function to display all games using In-Order traversal
void displayGames(struct AVLNode **root) {
    if (*root == NULL) {
        printf("Warehouse is empty!\n\n");
        ClearScreen();
        return;// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
    }

    printf("---------------------------------------------------------\n");
    printf("| %-25s | %-12s | %-10s |\n", "Game Title", "Game Genre", "Game Stock");
    printf("---------------------------------------------------------\n");
    inorderTraversal(*root);
    printf("\n");
	ClearScreen();
}

void updateStock(struct AVLNode **root) {
    char title[26];
    char updateType[10];
    int quantity;

    printf("Input game title: ");
    fgets(title, sizeof(title), stdin);
    title[strcspn(title, "\n")] = '\0'; 

    // Search for the game title in the AVL tree
    struct Game *gameToUpdate = search(*root, title);

    if (gameToUpdate == NULL) {
        printf("Data not found!\n\n");
        ClearScreen();
        return;
    }

    printf("Current stock: %d\n\n", gameToUpdate->stock);

    while (1) {
        printf("Input update type[add|remove][case insensitive]: ");
        scanf("%s", updateType);
        // Convert update type to lowercase (in the module REMOVE == remove)
        for (int i = 0; updateType[i]; i++) {
            updateType[i] = tolower(updateType[i]);
        }
        if (strcmp(updateType, "add") != 0 && strcmp(updateType, "remove") != 0) {
            printf("Invalid update type! Please enter 'add' or 'remove'.\n");
            continue;
        }
        break;
    }

    // Ask for quantity
    while (1) {
        if (strcmp(updateType, "remove") == 0) {
            printf("Input stock to remove[1-%d]: ", gameToUpdate->stock);
            scanf("%d", &quantity);// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
            if (quantity < 1 || quantity > gameToUpdate->stock) {
                printf("Invalid quantity! Please enter a number between 1 and %d.\n", gameToUpdate->stock);
                continue;
            }
        } else { // updateType is "add"
            printf("Input stock to add[>= 1]: ");
            scanf("%d", &quantity);
            if (quantity < 1) {
                printf("Invalid quantity! Please enter a number greater than or equal to 1.\n");
                continue;
            }
        }
        break;
    }

    // Update stock
    if (strcmp(updateType, "remove") == 0) {
        gameToUpdate->stock -= quantity;
        if (gameToUpdate->stock == 0) {
            *root = deleteGame(*root, gameToUpdate->title); // Delete the game if stock is 0
            printf("%s is removed from the warehouse !\n", gameToUpdate->title);
        }
    } else { // updateType is "add"
        gameToUpdate->stock += quantity;
    }

    printf("Data updated successfully !\n\n");
    getchar();
    ClearScreen();
}


int main() {
    int choice;
    struct AVLNode *root = NULL;
    
    do {// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
    	printf("Bluejack GShop\n");
	    printf("==============\n");
	    printf("1. Insert Game\n");
	    printf("2. View Game\n");
	    printf("3. Update Stock\n");
	    printf("4. Exit\n");
        printf(">> ");
        scanf("%d", &choice);
		
        // Clear input buffer
        while (getchar() != '\n');
		system("cls");
        switch(choice) {
            case 1:
                insertGame(&root);
                break;
            case 2:
                displayGames(&root);// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566
                break;
            case 3:
                 updateStock(&root);
                break;
            case 4:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice! Please enter a number between 1 and 4.\n\n");
				ClearScreen();
        }
    } while(choice != 4);
    
    return 0;
}
// Dibuat oleh Stanley Pratama Teguh dengan NIM: 2702311566

