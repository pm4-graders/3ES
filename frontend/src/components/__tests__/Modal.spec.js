import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Modal from '../Modal.vue'

describe('Modal', () => {
  it('renders with props', async () => {
    const wrapper = mount(Modal, {
      props: {
        show: true,
        title: 'Test Title'
      },
      slots: {
        default: '<p>Test Body</p>',
        footer: '<button>Test Footer</button>'
      }
    })

    expect(wrapper.html()).toContain('Test Title')
    expect(wrapper.html()).toContain('Test Body')
    expect(wrapper.html()).toContain('Test Footer')

    await wrapper.setProps({ show: false })
    expect(wrapper.html()).not.toContain('Test Title')
  })

  it('emits close event', async () => {
    const wrapper = mount(Modal, {
      props: {
        show: true
      }
    })

    await wrapper.find('.modal').trigger('click')
    expect(wrapper.emitted().close).toBeTruthy()
  })
})
