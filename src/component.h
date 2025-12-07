#include <iostream>
#include <memory>
#include <string>
#include <vector>

using std::string;
using std::unique_ptr;
using std::vector;

namespace Component {

class Component;
class Subcomponent {

  public:
    size_t x, y;
    unique_ptr<Component> component;
    Subcomponent(unique_ptr<Component> _component, size_t _x, size_t _y)
        : component(std::move(_component)), x(_x), y(_y) {
    }
};

class Component {
  public:
    vector<string> layout;
    size_t height, width;
    vector<Subcomponent> subcomponents;
    Component(size_t _height, size_t _width)
        : height(_height), width(_width), layout(_height, string(_width, ' ')) {
    }

    auto& operator[](size_t x) {
        return layout[x];
    }
    void draw_subcomponents() {
        for (auto& sub : subcomponents) {
            sub.component->draw();
            for (int i = 0; i < sub.component->height && i + sub.x < height; i++) {
                for (int j = 0; j < sub.component->width && j + sub.y < width; j++) {
                    (*this)[sub.x + i][sub.y + j] = (*sub.component)[i][j];
                }
            }
        }
    }
    virtual void draw() = 0;
    virtual ~Component() {
    }
};

// 自适应长度的单行文本框
class TextBoard : public Component {
    string name;

  public:
    TextBoard(string _name) : Component(3, _name.size() + 4), name(_name) {
        (*this)[0] = string(width, '*');
        (*this)[1] = "* " + name + " *";
        (*this)[2] = string(width, '*');
    }
    void draw() {
        (*this)[1] = "* " + name + " *";
    }
};

// 绘制图像示例
class CatImage : public Component {

  public:
    CatImage() : Component(3, 7) {
        // clang-format off
            layout = {
                " /\\_/\\",
                "( o.o )",
                " >   < "
            };
        // clang-format on
    }
    void draw() {
    }
};

class TestPage : public Component {
  private:
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

  public:
    TestPage() : Component(10, 30) {
        // 组件中添加子组件示例
        // 现在添加的方式有点复杂，需要修改
        // 添加顺序也是渲染优先级，从低到高
        subcomponents.emplace_back(std::make_unique<TextBoard>("Alice"), 1, 1);
        subcomponents.emplace_back(std::make_unique<TextBoard>("AutoMachineGun"), 5, 1);
        subcomponents.emplace_back(std::make_unique<CatImage>(), 1, 12);
    }
    void draw() {
        draw_border();
        draw_subcomponents();
    }
    void print() {
        draw();
        for (int i = 0; i < height; i++) {
            std::cout << (*this)[i] << "\n";
        }
        std::cout << std::endl;
    }
};

} // namespace Component
