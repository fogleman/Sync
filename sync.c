#include <math.h>
#include <stdlib.h>

#define kE 2.71828182846

typedef struct {
    int size;
    double threshold;
    double influence;
    double *values;
} Model;

double f(double x) {
    return 1.0 - pow(kE, -x);
}

double g(double y) {
    return y < 1.0 ? log(1.0 / (1.0 - y)) : 50.0;
}

void update(Model *model, double dt) {
    int n = model->size;
    int count = n * n;
    for (int i = 0; i < count; i++) {
        model->values[i] += dt;
    }
    int *seen = (int *)calloc(count, sizeof(int));
    while (1) {
        int done = 1;
        for (int i = 0; i < count; i++) {
            if (seen[i]) {
                continue;
            }
            if (f(model->values[i]) < model->threshold) {
                continue;
            }
            done = 0;
            seen[i] = 1;
            int x1 = i % n;
            int y1 = i / n;
            for (int j = 0; j < count; j++) {
                if (i == j) {
                    continue;
                }
                int x2 = j % n;
                int y2 = j / n;
                int dx = abs(x2 - x1);
                int dy = abs(y2 - y1);
                int d2 = dx * dx + dy * dy;
                model->values[j] =
                    g(f(model->values[j]) + model->influence / d2);
            }
        }
        if (done) {
            break;
        }
    }
    free(seen);
    for (int i = 0; i < count; i++) {
        if (f(model->values[i]) >= model->threshold) {
            model->values[i] = 0.0;
        }
    }
}
