from httpx import AsyncClient

import asyncio

import lxml.html

from datetime import datetime

import json

async def run():
    async with AsyncClient() as client:
        res = await client.get('https://br.investing.com/currencies/usd-brl-historical-data')

        html=lxml.html.fromstring(res.content)
        table=html.xpath('//table[@id="curr_table"]')[0]
        trs=table.xpath('./tbody/tr')

        # import ipdb; ipdb.set_trace()

        for tr in trs:
            tds = tr.xpath('./td/text()')
            date = tds[0]
            currency = tds[1].replace(',','.')
            body = {
                "date_quotation": str(datetime.strptime(date, '%d.%m.%Y')).replace(' ', 'T'),
                "real_currency": float(currency)
            }
            coi = json.dumps(body)
            # import ipdb; ipdb.set_trace()
            await client.post('http://127.0.0.1:8000/dolar-quotation/', data=coi)

if __name__ == '__main__':
    asyncio.run(run())
