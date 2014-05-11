# Jasmine snippets [![Build Status](https://api.travis-ci.org/caiogondim/jasmine-sublime-snippets.png?branch=master)](https://travis-ci.org/caiogondim/jasmine-sublime-snippets)

<img src="https://raw.github.com/caiogondim/jasmine-sublime-snippets/master/img/logo.png" alt="Jasmine snippets logo" align="right" width="256">

Jasmine is a behavior-driven development framework for testing JavaScript code.
It does not depend on any other JavaScript frameworks. It does not require a
DOM. And it has a clean, obvious syntax so that you can easily write tests. This
package is for Jasmine **version 2.0.0**.

To install through Package Control, search for **Jasmine**. If you
still don't have Package Control in Sublime Text, go get it. If you insist to
not install it, you can download the package and put it manually inside your
Pacakages directory. It should work but will not update automatically.


## Demo

Some of the snippets in the wild.

![](https://raw.github.com/caiogondim/jasmine-sublime-snippets/master/img/demo.gif)


## Snippets

Below is a list of all snippets currently supported on this package and the
triggers of each one. The **⇥** means the `TAB` key.

### Specs
- `describe`: desc⇥
- `it`: it⇥
- `afterEach`: ae⇥
- `beforeEach`: be⇥

### Expectations
- `expect`: exp⇥
- `expect().toBe`: tb⇥
- `expect().toBeCloseTo`: tbct⇥
- `expect().toBeDefined`: tbd⇥
- `expect().toBeFalsy`: tbf⇥
- `expect().toBeGreaterThan`: tbgt⇥
- `expect().toBeLessThan`: tblt⇥
- `expect().toBeNull`: tbn⇥
- `expect().toBeTruthy`: tbt⇥
- `expect().toBeUndefined`: tbu⇥
- `expect().toContain`: tc⇥
- `expect().toEqual`: te⇥
- `expect().toHaveBeenCalled`: thbc⇥
- `expect().toHaveBeenCalledWith`: thbcw⇥
- `expect().toMatch`: tm⇥
- `expect().toThrow`: tt⇥
- `expect().not.toBe`: nb⇥
- `expect().not.toBeCloseTo`: nct⇥
- `expect().not.toBeDefined`: nd⇥
- `expect().not.toBeFalsy`: nf⇥
- `expect().not.toBeGreaterThan`: ngt⇥
- `expect().not.toBeLessThan`: nlt⇥
- `expect().not.toBeNull`: nn⇥
- `expect().not.toBeTruthy`: nt⇥
- `expect().not.toBeUndefined`: nu⇥
- `expect().not.toContain`: nc⇥
- `expect().not.toEqual`: ne⇥
- `expect().not.toMatch`: nm⇥
- `expect().not.toThrow`: nt⇥
- `jasmine.any`: a⇥
- `jasmine.objectContaining`: oc⇥

### Spies
- `spyOn`: s⇥
- `spyOn.and.callThrough`: sct⇥
- `spyOn.and.returnValue`: srv⇥
- `spyOn.and.stub`: ss⇥
- `spyOn.and.throwError`: se⇥
- `spy.calls.all`: ca⇥
- `spy.calls.allArgs`: caa⇥
- `spy.calls.any`: ca⇥
- `spy.calls.argsFor`: caf⇥
- `spy.calls.count`: cc⇥
- `spy.calls.first`: cf⇥
- `spy.calls.mostRecent`: cmr⇥
- `spy.calls.reset`: cr⇥
- `createSpy`: cs⇥
- `createSpyObj`: cso⇥


## License
The MIT License (MIT)

Copyright (c) 2014 [Caio Gondim](http://caiogondim.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
