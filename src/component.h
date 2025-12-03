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
    NameBoard(string _name) : Component(3, _name.size() + 4), name(_name) {
        (*this)[0] = string(width, '*');
        (*this)[1] = "* " + name + " *";
        (*this)[2] = string(width, '*');
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
        subcomponents.push_back(Subcomponent(new NameBoard("Tom"), 0, 0));
        subcomponents.push_back(Subcomponent(new NameBoard("Alice"), 7, 10));
        subcomponents.push_back(Subcomponent(new NameBoard("Bobby"), 3, 10));
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
class BigerPage : public Component {
  private:
    vector<Subcomponent> subcomponents;

  public:
    BigerPage() : Component(25, 80) {
        subcomponents.reserve(10);
        subcomponents.push_back(Subcomponent(new Page(), 1, 1));
        subcomponents.push_back(Subcomponent(new Page(), 11, 1));
    }
    void draw_border() {
        for (int i = 0; i < height; i++) {
            (*this)[i][0] = '|';
            (*this)[i][width - 1] = '|';
        }
        for (int j = 0; j < width; j++) {
            (*this)[0][j] = '-';
            (*this)[height - 1][j] = '-';
        }
    }
    void draw() {
        draw_border();
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
