# damnboleto

<img src="https://i.imgflip.com/1mj0kf.jpg">

## Instalação

```
pip install damnboleto
```

Obs.: `damnboleto` utiliza a lib `pdftotext` que exige que algumas dependências estejam instaladas no SO. Consulte [aqui](https://github.com/jalan/pdftotext#os-dependencies).

## Uso

```
from damnboleto import Extractor

extractor = Extractor(filepath='/home/user/boleto.pdf')
print(extractor.extract_all())

{
    'boleto_number': '03399 63290 64000 000006 00125 201020 4 56140000017832', 
    'bank_code': '033',
    'bank': 'Banco Santander (Brasil) S.A.'
}
```

## Licença

MIT License

Copyright (c) 2018 marquesds

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