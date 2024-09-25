#include <iostream>
using namespace std;

struct Node {
    int data;
    int priority;
    int isActive; // New flag to indicate if the node is active
    Node* next;
};

class CircularPriorityQueue {
private:
    Node* front;
    Node* rear;

public:
    CircularPriorityQueue() {
        front = rear = nullptr;
    }

    ~CircularPriorityQueue() {
        while (front != nullptr) {
            dequeue();
        }
    }

    void enqueue(int data, int priority, int isActive = 1) {
        Node* temp = new Node();
        temp->data = data;
        temp->priority = priority;
        temp->isActive = isActive; // Set the isActive flag
        temp->next = nullptr;

        if (front == nullptr) {
            front = rear = temp;
            rear->next = front;
        } else {
            Node* start = front;

            if (front->priority > priority) {
                while (rear->next != front) {
                    rear = rear->next;
                }
                temp->next = front;
                front = temp;
                rear->next = front;
            } else {
                while (start->next != front && start->next->priority <= priority) {
                    start = start->next;
                }
                temp->next = start->next;
                start->next = temp;

                if (start == rear) {
                    rear = temp;
                }
            }
        }
    }

    void dequeue() {
        if (front == nullptr) {
            cout << "Queue is empty" << endl;
            return;
        }

        Node* temp = front;
        Node* prev = rear;

        do {
            if (temp->isActive == 1) {
                if (temp == front) {
                    if (front == rear) {
                        delete front;
                        front = rear = nullptr;
                    } else {
                        front = front->next;
                        rear->next = front;
                        delete temp;
                    }
                } else {
                    prev->next = temp->next;
                    if (temp == rear) {
                        rear = prev;
                    }
                    delete temp;
                }
                return;
            }
            prev = temp;
            temp = temp->next;
        } while (temp != front);

        cout << "No active elements to dequeue" << endl;
    }

    void display() {
        if (front == nullptr) {
            cout << "Queue is empty" << endl;
            return;
        }

        Node* temp = front;
        do {
            if (temp->isActive == 1) {
                cout << "Data: " << temp->data << " Priority: " << temp->priority << endl;
            }
            temp = temp->next;
        } while (temp != front);
    }
};