import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import Navbar from '../NavbarComponent.vue'

describe('Navbar', () => {
  it('renders the list of entries', () => {
    const list = [
      { title: 'Home', path: '/' },
      { title: 'About', path: '/about' },
      { title: 'Contact', path: '/contact' }
    ]
    const wrapper = mount(Navbar, {
      props: {
        list
      }
    })
    const entries = wrapper.findAll('[data-test="item"]')
    expect(entries.length).toBe(list.length)
    entries.forEach((entry, index) => {
      expect(entry.find('a').text()).toBe(list[index].title)
    })
  })
})
