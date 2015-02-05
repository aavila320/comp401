#include <vector>

using namespace std;

class Quadtree;
class Object;

class Quadtree {
public:
    Quadtree(float x, float y, float width, float height, int level, int maxLevel);
    ~Quadtree();

	void insertObject(Object *object);
	vector<Object*> GetObjects(float x, float y);
	void Clear();

private:
	float x;
	float y;
	float width;
	float height;
	int level;
	int	 maxLevel;
	vector<Object*>				objects;

	Quadtree *	parent;
	Quadtree * TopLeft;
	Quadtree * TopRight;
	Quadtree * BottomLeft;
	Quadtree * BottomRight;


	bool contains(Quadtree *child, Object *object);
};
