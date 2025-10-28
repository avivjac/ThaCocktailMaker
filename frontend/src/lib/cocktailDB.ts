// src/lib/cocktaildb.ts
import axios from 'axios'


const BASE = process.env.COCKTAILDB_BASE ?? 'https://www.thecocktaildb.com/api/json/v1'
const KEY = process.env.COCKTAILDB_KEY ?? '1'


export type Cocktail = {
idDrink: string
strDrink: string
strDrinkThumb: string
[k: string]: string | null | undefined
}

type CocktailDBResponse = {
drinks: Cocktail[] | null
}

export async function searchByName(q: string) {
const url = `${BASE}/${KEY}/search.php?s=${encodeURIComponent(q)}`
const { data } = await axios.get<CocktailDBResponse>(url)
return (data.drinks ?? []) as Cocktail[]
}


export async function filterByIngredient(ingredient: string) {
const url = `${BASE}/${KEY}/filter.php?i=${encodeURIComponent(ingredient)}`
const { data } = await axios.get<CocktailDBResponse>(url)
return (data.drinks ?? []) as Cocktail[]
}


export async function lookupById(id: string) {
const url = `${BASE}/${KEY}/lookup.php?i=${encodeURIComponent(id)}`
const { data } = await axios.get<CocktailDBResponse>(url)
return (data.drinks?.[0] ?? null) as Cocktail | null
}