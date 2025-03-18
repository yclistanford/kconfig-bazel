#include "myfeatures.h"
// #include "CONFIG_INT_VALUE.h"
// #include "CONFIG_FEATURE1.h"
// #include "CONFIG_FEATURE2.h"

#include <iostream>

int main() {
  std::cout << CONFIG_GREETING << CONFIG_INT_VALUE << std::endl;
#if CONFIG_FEATURE1 == 1
  runFeature1();
#endif
#if CONFIG_FEATURE2 == 1
  runFeature2();
#endif
  return 0;
}
