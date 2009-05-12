#include <Python.h>
#include <stdio.h>

static PyObject *
greet_greet(PyObject *self, PyObject *args)
{
   char *name;

   if (!PyArg_ParseTuple(args, "s", &name)) {
       return NULL;
   }

   printf("Hello %s\n", name);
 
   return Py_BuildValue("");
}

static PyMethodDef GreetMethods[] = {
   { "greet",  greet_greet, METH_VARARGS,
     "Print a friendly greeting."
   },
   {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_greet(void)
{
   Py_InitModule("_greet", GreetMethods);
}
