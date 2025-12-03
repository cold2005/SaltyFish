#include <iostream>
#include <memory>
#include <string>
#include <vector>

using std::string;
using std::vector;

class Component {
  private:
    vector<string> layout;

  public:
    size_t height, width;
    Component(size_t _height, size_t _width)
        : height(_height), width(_width), layout(_height, string(_width, ' ')) {
    }
    virtual void draw() = 0;
    auto& operator[](size_t x) {
        return layout[x];
    }
    virtual ~Component() {
    }
};

class Subcomponent {

  public:
    Component* component;
    size_t x, y;
    Subcomponent(Component* _component, int _x, int _y) : component(_component), x(_x), y(_y) {
    }
    ~Subcomponent() {
        // delete component;
        // delete 会导致重复释放，需要重新编写逻辑,先让它泄露吧🆒
    }
};

class NameBoard : public Component {
    string name;

  public:
    NameBoard(string _name) : Component(3, 13), name(_name) {
        (*this)[0] = "*************";
        (*this)[1] = "*           *";
        (*this)[2] = "*************";
    }
    void draw() {
        (*this)[1] = "* " + name + " *";
    }
};

class Page : public Component {
    vector<Subcomponent> subcomponents;

  public:
    Page() : Component(10, 30) {
        subcomponents.reserve(10);
        subcomponents.push_back(Subcomponent(new NameBoard("wallcrack"), 0, 0));
        subcomponents.push_back(Subcomponent(new NameBoard("windchime"), 8, 10));
    }
    void draw() {
        for (auto& sub : subcomponents) {
            sub.component->draw();
            for (int i = 0; i < sub.component->height && i + sub.x < height; i++) {
                for (int j = 0; j < sub.component->width && j + sub.y < width; j++) {
                    (*this)[sub.x + i][sub.y + j] = (*sub.component)[i][j];
                }
            }
        }
    }
    void print() {
        draw();
        for (int i = 0; i < height; i++) {
            std::cout << (*this)[i] << "\n";
        }
        std::cout << std::endl;
    }
};
