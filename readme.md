[CheckMATE](http://checkmate.hepforge.org/) 
=========

### Authors

   D. Schmeier, J. Tattersall, and J. S. Kim

### References

 * [Comput. Phys. Commun. **187** (2014) 227](http://dx.doi.org/10.1016/j.cpc.2014.10.018) [[1312.2591](http://arxiv.org/abs/1312.2591)].
 * https://checkmate.hepforge.org/
 * See [Code References](https://checkmate.hepforge.org/) for further references (citations).
    - Delphes 3
    - FastJet
    - Anti-kt jet algorithm
    - CLs prescription
    - mT2 family
    - mCT family

### Compile

```
git submodule init
git submodule update

cd vendor/delphes
./configure
make
cd ../..

./configure --with-delphes=`pwd`/vendor/delphes
make
```

Note: on macos, you may want to execute `install_name_tool -add_rpath $ROOTSYS/lib tools/fritz/bin/fritz` to avoid "dyld: Library not loaded: @rpath/libGui.so" errors.
